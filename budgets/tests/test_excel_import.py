from decimal import Decimal
from io import BytesIO

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from openpyxl import Workbook

from accounts.models import Organization
from budgets.importers import ExcelImportError, import_budget_from_excel
from budgets.models import BudgetHeader, BudgetItem, Budget
from construction.models import Construction, Order


def build_order():
    organization = Organization.objects.create(name="Alpha Build")
    construction = Construction.objects.create(name="Site A", organization=organization)
    return Order.objects.create(name="Order A", construction=construction)


def build_workbook_bytes(include_headers=True, include_header_rows=True):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Zakázka"
    if include_headers:
        sheet.append(["Poř.", "Typ", "Kód", "Popis", "MJ", "Výměra", "Jedn. Cena", "Cena"])
    if include_header_rows:
        sheet.append(["", "Stavba", "", "Stavba A", "", "", "", ""])
        sheet.append(["", "Oddíl", "", "Oddil 1", "", "", "", ""])
    sheet.append(["1", "SUB", "K-01", "Item 1", "m2", "10", "1\xa0234,50", ""])
    sheet.append(["", "", "Výkaz výměr:", "Detail", "", "", "", ""])
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()


def build_workbook_without_zakazka():
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Other"
    sheet.append(["Typ", "Popis"])
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()


@pytest.mark.django_db
def test_import_budget_creates_headers_and_items(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    order = build_order()
    payload = build_workbook_bytes()
    budget = Budget.objects.create(
        order=order,
        name="Budget A",
        excel_file=SimpleUploadedFile("budget.xlsx", payload),
    )

    created = import_budget_from_excel(budget)

    assert created == 1
    assert BudgetHeader.objects.filter(budget=budget).count() == 2
    header = BudgetHeader.objects.get(title="Oddil 1")
    assert header.parent.title == "Stavba A"
    item = BudgetItem.objects.get(header=header)
    assert item.code == "K-01"
    assert item.measure_unit == "m2"
    assert item.price_for_unit == Decimal("1234.50")


@pytest.mark.django_db
def test_import_requires_header_row(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    order = build_order()
    payload = build_workbook_bytes(include_headers=False)
    budget = Budget.objects.create(
        order=order,
        name="Budget B",
        excel_file=SimpleUploadedFile("budget.xlsx", payload),
    )

    with pytest.raises(ExcelImportError):
        import_budget_from_excel(budget)


@pytest.mark.django_db
def test_import_requires_zakazka_sheet(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    order = build_order()
    payload = build_workbook_without_zakazka()
    budget = Budget.objects.create(
        order=order,
        name="Budget C",
        excel_file=SimpleUploadedFile("budget.xlsx", payload),
    )

    with pytest.raises(ExcelImportError):
        import_budget_from_excel(budget)
