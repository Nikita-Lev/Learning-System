importScripts("https://cdn.jsdelivr.net/pyodide/v0.21.3/full/pyodide.js");

function sendPatch(patch, buffers, msg_id) {
  self.postMessage({
    type: 'patch',
    patch: patch,
    buffers: buffers
  })
}

async function startApplication() {
  console.log("Loading pyodide!");
  self.postMessage({type: 'status', msg: 'Loading pyodide'})
  self.pyodide = await loadPyodide();
  self.pyodide.globals.set("sendPatch", sendPatch);
  console.log("Loaded!");
  await self.pyodide.loadPackage("micropip");
  const env_spec = ['https://cdn.holoviz.org/panel/0.14.2/dist/wheels/bokeh-2.4.3-py3-none-any.whl', 'https://cdn.holoviz.org/panel/0.14.2/dist/wheels/panel-0.14.2-py3-none-any.whl', 'pyodide-http==0.1.0', 'random']
  for (const pkg of env_spec) {
    let pkg_name;
    if (pkg.endsWith('.whl')) {
      pkg_name = pkg.split('/').slice(-1)[0].split('-')[0]
    } else {
      pkg_name = pkg
    }
    self.postMessage({type: 'status', msg: `Installing ${pkg_name}`})
    try {
      await self.pyodide.runPythonAsync(`
        import micropip
        await micropip.install('${pkg}');
      `);
    } catch(e) {
      console.log(e)
      self.postMessage({
	type: 'status',
	msg: `Error while installing ${pkg_name}`
      });
    }
  }
  console.log("Packages loaded!");
  self.postMessage({type: 'status', msg: 'Executing code'})
  const code = `
  
import asyncio

from panel.io.pyodide import init_doc, write_doc

init_doc()

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import panel as pn
from random import randint, random
from panel.interact import interact, interactive, fixed, interact_manual
pn.extension()


# In[2]:


dirs = ['System_equations/', 'Power_equations/']

ind = 0
a, b = 0, 2
k = randint(a, b)

sysAnswers = [['3', '-2'], ['-1', '-2'], ['2', '3']]
PowerAnswers = ['3', '3.5', '0']


# In[3]:


ThemNames = ['System of Equations with Two Unknowns', 'Power equations']
ColumnNames = ['General scheme', 'Solution method', 'Training tasks', 'Control tasks']
nTh = len(ThemNames)
nColumn = len(ColumnNames)

columns = [[pn.Column()] * nColumn for i in range(nTh)]
columns[0][0] = pn.Column(pn.panel('system.jpg', width = 500))
columns[0][1] = pn.Column(pn.panel('substitution_general.jpg', width = 650), '### Solution Example', pn.panel('Substitution example.jpg', width = 700))
columns[0][2] = pn.Column()
columns[0][3] = pn.Column()

columns[1][0] = pn.Column(pn.panel('mental diagram PU.jpg', width = 600))
columns[1][1] = pn.Column(pn.panel('method for introducing a new variable.jpg', width = 600))
columns[1][2] = pn.Column()
columns[1][3] = pn.Column()


# In[4]:


select = pn.widgets.Select(name = 'Choose a theme', options={'System of Equations with Two Unknowns' : 0, 'Exponential equations' : 1})
Themes = pn.Column()
tabs = pn.Tabs()


# In[5]:



tem = []
for i in range (b+1):
    k = round(random() * b)
    while k in tem:
        k = round(random() * b)
    tem.append(k)



# In[6]:



Xinput, Yinput = pn.widgets.TextInput( placeholder='X', max_length = 3, width = 40), pn.widgets.TextInput( placeholder='Y', max_length = 2, width = 40)
xy = pn.Row(Xinput, pn.Spacer(width = 15), Yinput)


# In[7]:


g = 0


# In[8]:


def outSolution(event):
    columns[0][2].append(pn.panel(dirs[0] + f'{tem[g]} solution.jpg', width = 600))


# In[9]:


showSolution = pn.widgets.Button(name = 'Show Solution', width = 50)
showSolution.on_click(outSolution)


# In[10]:


def ResultCheck(event):
    if Xinput.value_input  == sysAnswers[tem[g]][0] and Yinput.value_input == sysAnswers[tem[g]][1]:
        columns[0][2].append(f'#### Right!')
    else:
        columns[0][2].append(f'#### Wrong, try again.')
        columns[0][2].append(showSolution)
    


# In[11]:


def SysTrainView():
    
    columns[0][2].append('#### Solve System of Equations')
        
    columns[0][2].append(pn.panel(dirs[0] +  f'{tem[g]}.jpg', width = 200))
    

    check = pn.widgets.Button(name = 'Check', width=50)
    check.on_click(ResultCheck)
    
    change = pn.widgets.Button(name = 'Solve another', width = 50)
    change.on_click(changeExample)
    
    input_check = pn.Column(xy, pn.Row(check, pn.Spacer(width = 50), change))

    columns[0][2].append(input_check)


# In[12]:


def changeExample(event):
    columns[0][2].clear()
    
    global g
    g+=1
    
    if g == b+1:
        columns[0][2].append('#### All examples solved')
    else:
        SysTrainView()


# In[13]:


SysTrainView()



# In[14]:


XinputC, YinputC = pn.widgets.TextInput( placeholder='X', max_length = 3, width = 40), pn.widgets.TextInput( placeholder='Y', max_length = 2, width = 40)
xyC = pn.Row(XinputC, pn.Spacer(width = 15), YinputC)


# In[15]:


score = []
countS = 0


# In[16]:


def CheckTest(event):
    columns[0][3].clear()
    
    global score
    global countS
    
    if XinputC.value_input  == sysAnswers[tem[countS]][0] and YinputC.value_input == sysAnswers[tem[countS]][1]:
        score.append(1)
    else:
        score.append(0)
    countS += 1
    
    if countS == b+1:
        columns[0][3].append('#### Test results:')
        r = 0
        for i in range(b+1):
            s = f'Task {i+1}:'
            if score[i] == 1:
                r += 1
                s += ' right'
            else:
                s += ' wrong'
            columns[0][3].append(s)
        right = sum(score)
        al = len(score)
        columns[0][3].append(f'#### Your test result : {right} из {al} или {round(right / al * 100, 1)}%')
    else:
        SysTestView()


# In[17]:


def SysTestView():
    
    columns[0][3].append('#### Solve System of Equations')
    columns[0][3].append(pn.panel(dirs[0] +  f'{tem[countS]}.jpg', width = 200))
    
    attest = pn.widgets.Button(name = 'Confirm', width=50)
    attest.on_click(CheckTest)
    
    input_checkC = pn.Column(xyC, attest)

    columns[0][3].append(input_checkC)


# In[18]:


SysTestView()



# In[19]:


Xpower = pn.widgets.TextInput( placeholder='X', max_length = 3, width = 50)


# In[20]:


g = 0


# In[21]:


def outSolutionP(event):
    columns[1][2].append(pn.panel(dirs[1] + f'{tem[g]} solution.jpg', width = 600))


# In[22]:


showSolutionP = pn.widgets.Button(name = 'Show solution', width = 50)
showSolutionP.on_click(outSolutionP)


# In[23]:


def ResultCheckP(event):
    if Xpower.value_input  == PowerAnswers[tem[g]]:
        columns[1][2].append(f'#### Right!')
    else:
        columns[1][2].append(f'#### Wrong, try again.')
        columns[1][2].append(showSolutionP)
    


# In[24]:


def PowerTrainView():
    
    columns[1][2].append('#### Solve the exponential equation')
        
    columns[1][2].append(pn.panel(dirs[1] +  f'{tem[g]}.jpg', width = 165))
    
    
    checkP = pn.widgets.Button(name = 'Check', width=50)
    checkP.on_click(ResultCheckP)
    
    changeP = pn.widgets.Button(name = 'Solve another', width = 50)
    changeP.on_click(changeExampleP)
    
    input_checkP = pn.Column(Xpower, pn.Row(checkP, pn.Spacer(width = 50), changeP))

    columns[1][2].append(input_checkP)


# In[25]:


def changeExampleP(event):
    columns[1][2].clear()
    
    global g
    g+=1
    
    if g == b+1:
        columns[1][2].append('#### All examples solved')
    else:
        PowerTrainView()


# In[26]:


PowerTrainView()



# In[27]:


XpowerC = pn.widgets.TextInput( placeholder='X', max_length = 3, width = 50)


# In[28]:


scoreP = []
countSP = 0


# In[29]:


def CheckTestP(event):
    columns[1][3].clear()
    
    global scoreP
    global countSP
    
    if XpowerC.value_input  == PowerAnswers[tem[countSP]]:
        scoreP.append(1)
    else:
        scoreP.append(0)
    countSP += 1
    
    if countSP == b+1:
        columns[1][3].append('#### Test results:')
        r = 0
        for i in range(b+1):
            s = f'Задание {i+1}:'
            if scoreP[i] == 1:
                r += 1
                s += ' right'
            else:
                s += ' wrong'
            columns[1][3].append(s)
        right = sum(scoreP)
        al = len(scoreP)
        columns[1][3].append(f'#### Your test result : {right} из {al} или {round(right / al * 100, 1)}%')
    else:
        SysTestViewP()


# In[30]:


def SysTestViewP():
    
    columns[1][3].append('#### Solve the exponential equation')
        
    columns[1][3].append(pn.panel(dirs[1] +  f'{tem[countSP]}.jpg', width = 165))
    
    attestP = pn.widgets.Button(name = 'Confirm', width=50)
    attestP.on_click(CheckTestP)
    
    input_checkCP = pn.Column(XpowerC, attestP)

    columns[1][3].append(input_checkCP)


# In[31]:


SysTestViewP()



# In[32]:


# Выбор темы
def ThemeChoice(event):
    choiceTheme = select.value
    
    Themes.clear()
    Themes.append(pn.Column('### ' + ThemNames[choiceTheme]))
    
    tabs.clear()
    for i in range(nColumn):
        tabs.append((ColumnNames[i], columns[choiceTheme][i]))
    Themes.append(tabs)


# In[33]:


select.param.watch(ThemeChoice, 'value')
demo = pn.Column(select, Themes)


# In[34]:


demo.servable()



await write_doc()
  `

  try {
    const [docs_json, render_items, root_ids] = await self.pyodide.runPythonAsync(code)
    self.postMessage({
      type: 'render',
      docs_json: docs_json,
      render_items: render_items,
      root_ids: root_ids
    })
  } catch(e) {
    const traceback = `${e}`
    const tblines = traceback.split('\n')
    self.postMessage({
      type: 'status',
      msg: tblines[tblines.length-2]
    });
    throw e
  }
}

self.onmessage = async (event) => {
  const msg = event.data
  if (msg.type === 'rendered') {
    self.pyodide.runPythonAsync(`
    from panel.io.state import state
    from panel.io.pyodide import _link_docs_worker

    _link_docs_worker(state.curdoc, sendPatch, setter='js')
    `)
  } else if (msg.type === 'patch') {
    self.pyodide.runPythonAsync(`
    import json

    state.curdoc.apply_json_patch(json.loads('${msg.patch}'), setter='js')
    `)
    self.postMessage({type: 'idle'})
  } else if (msg.type === 'location') {
    self.pyodide.runPythonAsync(`
    import json
    from panel.io.state import state
    from panel.util import edit_readonly
    if state.location:
        loc_data = json.loads("""${msg.location}""")
        with edit_readonly(state.location):
            state.location.param.update({
                k: v for k, v in loc_data.items() if k in state.location.param
            })
    `)
  }
}

startApplication()