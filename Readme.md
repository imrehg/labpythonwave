# LabPythonWave

Using Python script to generate experimental waveforms in LabView.

Currently it's all done within LabView, external scripting has the flexibility to adjust to different input data formats, or extending current methods, as well as being faster than LabView's own generation.

The external CSV is still used for input. Output is into 2D array within LabView.

Have to supply the path to the script and to the CSV file.


## Install

Software to install:

* [Python][python] (2.7.3 at the moment, 32-bit) and [Numpy][numpy] (1.7.0).
* [VI Package Manager][vipm], from its homepage or from the NI website
* [LabPython][labpython] (from within the VI Package Manager)
* [OpenG][openg] (optional) (from within the VI Package Manager)

Settings:

* Use "PYTHON Set Server Path" sub-VI to set the correct path, usually: `C:\Windows\System32\python27.dll`

## Known issues

* Might need to set up first the apporpriate Python path within Labview (find e.g. C:\Windows\System32\python27.dll)
* Ramp shapes other than linear are not implemented
* Looping not implemented

[python]: http://www.python.org/getit/ "Python Download Page"
[numpy]: http://sourceforge.net/projects/numpy/files/NumPy/ "Numpy download files"
[vipm]: http://jki.net/vipm "VI Package Manager homepage"
[openg]: http://sine.ni.com/nips/cds/view/p/lang/en/nid/209027 "OpenG on National Instruments homepage"
[labpython]: http://labpython.sourceforge.net/ "LabPython homepage"
