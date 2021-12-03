import random
import pandas as pd
import xlsxwriter
"""
https://pandas-xlsxwriter-charts.readthedocs.io/chart_legend_stock.html
"""



def test_xlswriter():
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook('demo.xlsx')
    worksheet = workbook.add_worksheet()

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 20)

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})

    # Write some simple text.
    worksheet.write('A1', 'Hello')

    # Text with formatting.
    worksheet.write('A2', 'World', bold)

    # Write some numbers, with row/column notation.
    worksheet.write(2, 0, 123)
    worksheet.write(3, 0, 123.456)

    # Insert an image.
    worksheet.insert_image('B5', 'logo.png')

    workbook.close()


def _create_chart_column(workbook):
    # Create a chart object.
    chart = workbook.add_chart({'type': 'column'})

    # Configure the series of the chart from the dataframe data.
    chart.add_series({
        'values': ['Sheet1', 1, 1, 7, 1],
        'gap': 2,
    })

    # Configure the chart axes.
    chart.set_x_axis({'name': 'Index', 'num_font': {'rotation': 45}})
    chart.set_y_axis({'name': 'Value', 'major_gridlines': {'visible': False}})

    # Turn off chart legend. It is on by default in Excel.
    chart.set_legend({'position': 'none'})
    return chart


def _create_chart_line(workbook):
    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': ['Sheet1', 1, 0, 7, 0],
        'values':     ['Sheet1', 1, 1, 7, 1],
    })

    # Configure the chart axes.
    chart.set_x_axis({'name': 'Index', 'position_axis': 'on_tick', 'num_font': {'rotation': 45}})
    chart.set_y_axis({'name': 'Value', 'major_gridlines': {'visible': False}})

    # Turn off chart legend. It is on by default in Excel.
    chart.set_legend({'position': 'none'})
    return chart




def test_pd_execl():
    # Create a Pandas dataframe from the data.
    df = pd.DataFrame([10, 20, 30, 20, 15, 30, 45])

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('simple.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')

    # Get the xlsxwriter objects from the dataframe writer object.
    workbook = writer.book
    # chart = _create_chart_column(workbook)
    chart = _create_chart_line(workbook)
    # # Insert the chart into the worksheet.
    worksheet = writer.sheets['Sheet1']
    worksheet.insert_chart('D2', chart)
    writer.save()


def _create_chart_legends(workbook, cat_1):

    # Create a chart object.
    chart = workbook.add_chart({'type': 'line'})
    # Configure the series of the chart from the dataframe data.
    for i in range(len(cat_1)):
        col = i + 1
        chart.add_series({
            'name': ['Sheet1', 0, col],
            'categories': ['Sheet1', 1, 0, 21, 0],
            'values': ['Sheet1', 1, col, 21, col],
        })

    # Configure the chart axes.
    chart.set_x_axis({'name': 'Index'})
    chart.set_y_axis({'name': 'Value', 'major_gridlines': {'visible': False}})
    return chart


def test_pd_execl_mul():
    # Some sample data to plot.
    cat_1 = ['y1', 'y2', 'y3', 'y4']
    index_1 = range(0, 21, 1)
    multi_iter1 = {'index': index_1}
    for cat in cat_1:
        multi_iter1[cat] = [random.randint(10, 100) for _ in index_1]

    # Create a Pandas dataframe from the data.
    index_2 = multi_iter1.pop('index')
    df = pd.DataFrame(multi_iter1, index=index_2)
    df = df.reindex(columns=sorted(df.columns))

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    excel_file = 'legend.xlsx'
    sheet_name = 'Sheet1'

    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name)

    # Access the XlsxWriter workbook and worksheet objects from the dataframe.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    chart = _create_chart_legends(workbook, cat_1)
    # Insert the chart into the worksheet.
    worksheet.insert_chart('G2', chart)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


if __name__ == '__main__':
    # test_xlswriter()
    # test_pd_execl()
    test_pd_execl_mul()