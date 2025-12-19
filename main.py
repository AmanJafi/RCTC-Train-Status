import requests
from bs4 import BeautifulSoup
import gradio as gr

stations=[]

def getInfo(trainNum):
  global stations
  url=f"https://www.railyatri.in/live-train-status/{trainNum}"
  res = requests.get(url)
  soup = BeautifulSoup(res.text,"html.parser")
  data=soup.find_all("td")
  
  class station:
    def __init__(self, NAME, TOA, HALTTIME):
      self.name = NAME
      self.timeOfArrival = TOA
      self.haltTime = HALTTIME

  stations=[]

  c=1
  l=[]
  for i in data:
    l.append(i.text)
    if c>5:
      c=0
      daob=station(l[0],l[1],l[3])
      stations.append(daob)
      l=[]
    c+=1
  if not stations:
    return "Invalid Train Number!",gr.Column(visible=False),"",""
  trainName = soup.find_all("h3")[0].text.strip()[0:-26]
  return f"Got Info!: {trainName}",gr.Column(visible=True),"",""


def search(stationName):
  global stations
  resstr=""
  flag = False
  for i in stations:
    if stationName.lower() in i.name.lower():
      resstr+= (f"Found {i.name.capitalize()}: {i.timeOfArrival} for {i.haltTime}\n")
      flag=True
  if not flag:
    return "Not Found"
  else:
    return resstr


# #the train name 
# print(soup.find_all("h3")[0].text.strip()+"\n\n")


with gr.Blocks() as demo:
    gr.Markdown("Train Finder")
    trNo = gr.Number(label="Train Number")
    status = gr.Textbox(label="status")
    submit_btn = gr.Button(value="Submit")
    with gr.Column(visible=False) as StationManager:
      stat_name = gr.Text(label="Station Name")
      output = gr.TextArea(label="Station Details")
      
    def hide_manager():
        return gr.Column(visible=False), "", "", ""

    trNo.change(
        fn=hide_manager, 
        inputs=None, 
        outputs=[StationManager, status, stat_name, output]
    )
    trNo.submit(fn=getInfo,inputs=trNo,outputs=[status,StationManager,stat_name,output])
    submit_btn.click(fn=getInfo,inputs=trNo,outputs=[status,StationManager,stat_name,output])
    stat_name.change(fn=search,inputs=stat_name,outputs=output)
    

demo.launch()

# print(getInfo(int(input())))
# print(search(input()))