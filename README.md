# UE4PyServer
<h2>Unreal Engine Python Plugin</h2>
<h3>Installation: (For now Linux Only)</h3><br/>
<h4>Prerequisits</h4>
- Unreal Engine for linux installation:  <a href="https://wiki.unrealengine.com/Building_On_Linux">UE4</a><br/>
- Python 3.x installation<br/>
For the purpose of the demo I installed python 3.5 Anaconda <a href="https://www.continuum.io/downloads" >Anaconda</a>. <br/>
<h4>Prerequisits For Otical-Flow Demo</h4>
- OpenCv for Python 3<br/>
conda install -c menpo opencv3<br/>
- numpy<br/>
conda install numpy 

<h4>Plugin Setup</h4>
- Create a project in unreal engine:<br/>
- Add an empty c++ class so the project will be a code project<br/>
- Close the project<br/>
- In the project dir create Plugin dir<br/>
- Clone UE4PyServer to that dir<br/>
git clone  https://github.com/orig74/UE4PyServer.git<br/>
- cd to:  [ProjectPath]/Plugins/UE4PyServer/Source/PyServer<br/>
- run: <br/>
python config.py --entry_point \<your entry point\><br/>
for the test demo run:<br/>
python config.py --entry_point track_test
- run:<br/>
python build.py --engine-path=\<unreal engine dir PATH\><br/>

<h4>Running minimal example:</h4>
- Set entry point for the minimal file<br/>
python config.py --entry_point minimal<br/>
the minimal file is minimal.py<br/>
- Add "PyServerTickActor":<br/>
Press the Plugin button PyServer.  PyServerTickActor will apear in the Outliner pannel in the right.<br/>
- Play:<br/>
Press the play button in Play button in the Toolbar. The supporting mode are:  "Selected ViewPort"  and "New Editor Window" 

<h4>Running The Demo:</h4>
The demo is "Lucas-Kanade optical flow tracking" from OpenCV library. <br/>
- Add Camera CameraActor_2  and a WindDirectionalSource:<br/>
In the Modes Pannel in the Place Tab add a Camera Actor. Change The name of the actor to "CameraActor_2".<br/>
In the Modes Pannel in the Place Tab add a WindDirectionalSource. Change The name to "WindDirectionalSource1"<br/>
- Add "PyServerTickActor":<br/>
Press the Plugin button PyServer.  PyServerTickActor will apear in the Outliner pannel in the right.<br/>
- Play:<br/>
Press the play button in Play button in the Toolbar. The supporting mode are:  "Selected ViewPort"  and "New Editor Window" <br/>
Focus on the engine window to get 30 fps!!<br/>
Watch demo on: <a href="https://youtu.be/ydBFlI_fhso">demo</a><br/>
This <a href="https://youtu.be/nXu6NCOoIRQ">demo</a> uses a SceneCapture2D and a Render Target to play inside an OpenCV window.

<h4>Limitations:</h4>
For now, the demo can only run in the Editor mode, so it right for research but not much useful for game development. The reason for that is that the screen capture is done outside the Draw function of the FViewPort Class. 

