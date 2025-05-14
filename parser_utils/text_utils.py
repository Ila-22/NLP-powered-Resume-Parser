def split_columns(lines):
    column_1 = [line['left'] for line in lines if line['left'].strip()]
    column_2 = [line['right'] for line in lines if line['right'].strip()]
    return column_1, column_2
