# Import relevant packages
import os, math, sys, argparse
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly

# Main function
def main():
  # Version info
  vers = "JoSIM Trace Plotting Script - 1.3 - CSV/DAT plotting script"

  # Initiate the parser
  parser = argparse.ArgumentParser(description=vers)

  # Add possible parser arguments
  parser.add_argument("input", help="the CSV input file")
  parser.add_argument("-o", "--output", help="the output file name with supported extensions: png, jpeg, webp, svg, eps, pdf")
  parser.add_argument("-x", "--html", help="save the output as an html file for later viewing")
  parser.add_argument("-t", "--type", help="type of plot: grid, stacked, combined, square. Default: grid", default="grid")
  parser.add_argument("-s", "--subset", nargs='+', help="subset of traces to plot. specify list of column names (as shown in csv file header), ie. \"V(1)\" \"V(2)\". Default: None")
  parser.add_argument("-c", "--color", help="set the output plot color scheme to one of the following: light, dark, presentation. Default: dark", default='dark')
  parser.add_argument("-w", "--title", help="set plot title to the provided string")
  parser.add_argument("-V", "--version", action='version', help="show script version", version=vers)

  # Read arguments from the command line
  args = parser.parse_args()

  outformats = [".png", ".jpeg", ".webp", ".svg", ".eps", ".pdf"]

  if (os.path.splitext(args.input)[1] == ".csv"):
    df = pd.read_csv(args.input, sep=',')
  elif (os.path.splitext(args.input)[1] == ".dat"):
    df = pd.read_csv(args.input, delim_whitespace=True)
  else:
    print("Invalid input file specified: " + args.input)
    print("Please provide either .csv (comma seperated) or .dat (space seperated) file")
    sys.exit()

  if(args.type == "grid"):
    fig = grid_layout(df, args.subset)
  elif(args.type == "stacked"):
    fig = stacked_layout(df, args.subset)
  elif(args.type == "combined"):
    fig = combined_layout(df, args.subset)
  elif(args.type == "square"):
    fig = square_layout(df, args.subset)
  else:
    print("Invalid plot type specified: " + args.type)
    print("Please provide either gird, stacked or combined as type")
    sys.exit()

  if(args.color == 'light'):
    template = 'plotly_white'
  elif(args.color == 'dark'):
    template = 'plotly_dark'
  elif(args.color == 'presentation'):
    template = 'presentation'
  else:
    print("Invalid plot color specified: " + args.color)
    print("Please provide either light, dark or presentation as color theme")
    sys.exit()
    
  if(args.title == None):
    title=os.path.splitext(os.path.basename(args.input))[0]
  else:
    title=args.title

  fig.update_layout(
    title=title,
    title_font_size=30,
    template=template
  )
  config = dict({
    'scrollZoom': True,
    'displaylogo': False
  })

  if(args.output == None and args.html == None):
    fig.show(config=config)
  elif(args.html != None and args.output == None):
    fig.write_html(args.html)
  elif(args.html == None and os.path.splitext(args.output)[1] in outformats):
    fig.write_image(args.output, width=3508, height=2480)
  else:
    print("Unknown file format for output file specified.")
    print("Please use: png, jpeg, webp, svg, eps or pdf")  

# Function that sets the Y-axis title relevant to the data
def y_axis_title(figLabel):
  if figLabel[0] == 'V':
    return "(V)"
  elif figLabel[0] == 'I':
    return "(A)"
  elif figLabel[0] == 'P':
    return ""
  else:
    return "Unknown"

# Return a grid of plots
def grid_layout(df, subset):
  plots = df.columns[1:].tolist() if subset == None else subset
  fig = make_subplots(
    rows=len(plots), 
    cols= 1,
    subplot_titles=plots,
    horizontal_spacing=0.075,
    vertical_spacing=0.4/len(plots),
    x_title= 't(s)')
  # Add the traces
  for i in range(0, len(plots)):
    col = 1
    row = i+1
    fig.add_trace(go.Scatter(
      x=df.iloc[:,0], y=df.loc[:,plots[i]],
      mode='lines',
      name=plots[i]),
      row=row,
      col=col
    )
    fig.layout.annotations[i].x = 0.985
    if i == 0:
      fig['layout']['yaxis']['title']=y_axis_title(plots[i])
    else:
      fig['layout']['yaxis' + str(i+1)]['title']=y_axis_title(plots[i])
  return fig

# Return a square of plots
def square_layout(df, subset):
  plots = df.columns[1:].tolist() if subset == None else subset
  square = math.sqrt(len(plots))
  row = int(round(square))
  col = int(math.ceil(square))
  fig = make_subplots(
    rows=row, 
    cols=col,
    subplot_titles=plots,
    horizontal_spacing=(0.25/row),
    vertical_spacing=(0.25/col),
    x_title= 'Time (seconds)')
  row_counter = 1
  col_counter = 1
  # Add the traces
  for i in range(0, len(plots)):
    if(i >= row_counter * math.ceil(square)):
      row_counter += 1
      col_counter = 1
    col = col_counter
    row = row_counter
    fig.add_trace(go.Scatter(
      x=df.iloc[:,0], y=df.loc[:,plots[i]],
      mode='lines',
      name=plots[i]),
      row=row,
      col=col
    )
    an_pos = 1 / math.ceil(square)
    fig.layout.annotations[i].x = an_pos * col_counter - 0.5 * an_pos
    fig.update_yaxes(row=row_counter, col=col_counter, title_standoff=0, ticks="")
    fig.update_layout()
    if i == 0:
      fig['layout']['yaxis']['title']=y_axis_title(plots[i])
    else:
      fig['layout']['yaxis' + str(i+1)]['title']=y_axis_title(plots[i])
    col_counter += 1
  return fig

# Return a stack of plots
def stacked_layout(df, subset):
  plots = df.columns[1:].tolist() if subset == None else subset
  fig = make_subplots(
    rows=len(plots), 
    cols=1,
    subplot_titles=plots,
    vertical_spacing=0.2/math.ceil(len(plots)/2),
    x_title= 'Time (seconds)')
  # Add the traces
  for i in range(0, len(plots)):
    fig.add_trace(go.Scatter(
      x=df.iloc[:,0], y=df.loc[:,plots[i]],
      mode='lines',
      name=plots[i]),
      row=i + 1,
      col=1
    )
    fig.layout.annotations[i].x = 0.985
    if i == 0:
      fig['layout']['yaxis']['title']=y_axis_title(plots[i])
    else:
      fig['layout']['yaxis' + str(i+1)]['title']=y_axis_title(plots[i])
  return fig

# Combine all the plots
def combined_layout(df, subset):
  plots = df.columns[1:].tolist() if subset == None else subset
  fig = go.Figure()
  # Add the traces
  for i in range(0, len(plots)):
    fig.add_trace(go.Scatter(
      x=df.iloc[:,0], y=df.loc[:,plots[i]],
      mode='lines',
      name=plots[i])
    )
  return fig

if __name__ == '__main__':
  main()
