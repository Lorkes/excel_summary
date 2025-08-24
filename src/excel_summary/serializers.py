from rest_framework import serializers

from excel_summary.validators import xlsx_file


class SummarySerializer(serializers.Serializer):
    file = serializers.FileField(
        required=True,
        help_text="Excel spreadsheet (.xlsx) file to analyze",
        validators=[xlsx_file],
    )
    columns = serializers.CharField(
        required=True,
        help_text=(
            "Semicolon(;)-separated list of column names to summarize, "
            "ex: USD;CURRENT USD;CAD. "
            "Column name should match value in the cell (case-insensitive). "
            "The preferred approach is to just copy-paste values "
            "instead of typing to avoid typos. WARNING: results might be "
            "inaccurate if the provided column name is in a merged cell"
        ),
    )
