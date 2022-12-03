<div align="center">
  
# `🤖 Aimm (AI Model Manager)`
### **Tool for managing AI Models that works like pip<sup><sub>TM</sub></sup> or npm<sup><sub>TM</sub></sup>**
###  Pre-release alpha: [Downloads - AIModels.org](https://aimodels.org/download)
</div>

## 📖 Table of Contents

- [📝 Description](#-description)
- [📦 Installation](#-installation)
- [💻 Quickstart](#-quickstart)
- [👩‍💻 GUI](#-gui)
- [📚 Documentation](#-documentation)
- [📜 License](#-license)

## 📝 Description

AI Model Manager, it's like pip or npm - but for AI models!

#### User Benefits 
* Save disk space, potentially many gigabytes 
* No more having to hunt for a model and making sure you rename it and put it in the correct folder
* Less effort needed to audit what models are installed and where they came from 

#### Developer Benefits
* Less code to manage, no longer need to handle keeping model list and download logic
* Pickle scaning and security mechanisms will be built into app 


![image](https://user-images.githubusercontent.com/654993/205424825-a50d913d-0168-4d87-844f-ef376a3c8164.png)

## 📦 Installation

Visit [Downloads - AIModels.org](https://aimodels.org/download) and select and install the version right for you. (This is still pre-release alpha)

## 💻 Quickstart

First we have to initialize the aimodels.json file in the local folder

```bash
aimm init
```

Search for a model you want to use. For example the BSRGAN model, a super resolution model that can upscale images.

```bash
aimm search BSRGAN
```

Then we install and add it to a local aimodels.json file to keep track of all the models you use in your project.

```bash
aimm add BSRGAN
```

## 👩‍💻 GUI

The GUI is developed but not ready for release yet. 

![image](https://user-images.githubusercontent.com/654993/205428740-742bc94e-6426-4315-ae4f-72ef858c5638.png)

This will allow modules such as stable horde to be integrated.

## 📚 Documentation

[Documentation](https://docs.aimodels.org/es/AIMM/gettingstarted/)

## 📜 License

[Apache License 2.0](./LICENSE.md)
