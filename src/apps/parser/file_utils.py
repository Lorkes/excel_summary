from decimal import Decimal, InvalidOperation

import openpyxl
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

# usually headers shouldn't be far from top, so 10 should be enough for most cases
# can be adjusted based on more samples
HEADER_ROW_INDEX_LIMIT = 10
SUM_FORMULA_PREFIX = "=SUM"
AVG_FORMULA_PREFIX = "=AVERAGE"


def process_file(file: InMemoryUploadedFile | TemporaryUploadedFile, columns_to_summarize: list[str]) -> list[dict]:
    summary = []
    wb = openpyxl.load_workbook(file)
    for sheet in wb.worksheets:
        summary.extend(_summarize_columns(sheet, columns_to_summarize))
    for column in columns_to_summarize:
        if column not in [v["column"] for v in summary]:
            summary.extend(_get_columns_summary(column, [[]]))
    return summary


def _summarize_columns(sheet: Worksheet, columns_to_summarize: list[str]) -> list[dict]:
    summary: list[dict] = []
    for row in sheet.iter_rows(max_row=HEADER_ROW_INDEX_LIMIT):
        # get rid of redundant spaces to match selected columns
        # converting to str to allow selecting cells with numeric header
        # Nones are excluded via if cell.value
        row_values = [str(cell.value).strip().lower() if cell.value else cell.value for cell in row]
        # we assume that column names/header are never split into different rows
        # so as soon as we find at least single value - stop parsing rows below
        # if not all values are present in given row - either its a typo or wrong sheet
        is_header_found = False
        for col in columns_to_summarize:
            # preserving original values to return them to user
            # but comparing case-insensitive to avoid typos
            if col.lower() in row_values:
                # cannot use row.index, as we can have multiple results
                # dropping merged cells - requires guessing which column/row is the "correct" one
                cells: list[Cell] = [
                    row[idx]  # type: ignore[misc]
                    for idx, val in enumerate(row_values)
                    if val == col.lower() and isinstance(row[idx], Cell)
                ]
                # need to summarize only data after header
                header_row = cells[0].row
                column_letters: list[str] = [cell.column_letter for cell in cells]
                selected_columns = []
                for letter in column_letters:
                    # remove all rows prior to header and get rid of invalid data
                    column_data = _parse_column(sheet[letter][header_row:])
                    selected_columns.append(column_data)
                summary.extend(_get_columns_summary(col, selected_columns))
                is_header_found = True
        if is_header_found:
            break
    return summary


def _parse_column(column: tuple[Cell]) -> list[Decimal]:
    # get rid of empty rows and sum/avg formulas
    non_empty_values = [
        cell.value
        for cell in column
        if cell.value and not str(cell.value).startswith((SUM_FORMULA_PREFIX, AVG_FORMULA_PREFIX))
    ]
    result = []
    # make sure we have valid values to summarize
    # depending on requirements might be a good idea to calculate percentage of
    # valid/invalid values to decide whether we've chosen a correct column
    # for example, if >50% cells contain non-numeric data - abort summarizing
    for val in non_empty_values:
        try:
            result.append(Decimal(str(val)))
        except InvalidOperation:
            pass
    return result


def _get_columns_summary(column_name: str, selected_columns: list[list[Decimal]]) -> list[dict]:
    """
    Make summary from lists of extracted cells values
    """
    summary: list[dict] = []
    for column in selected_columns:
        if not column:
            summary.append({"column": column_name, "sum": "N/A", "avg": "N/A"})
        else:
            column_sum = sum(column, Decimal())
            column_avg = (column_sum / len(column)).quantize(Decimal("0.00001"))
            summary.append({"column": column_name, "sum": column_sum, "avg": column_avg})
    return summary
