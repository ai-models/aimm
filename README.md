<div align="center">
  
# `🤖 Aimm (AI Model Manager)`
### **Tool for managing AI Models that works like pip<sup><sub>TM</sub></sup> or npm<sup><sub>TM</sub></sup>**
###  Pre-release alpha: [Downloads - AIModels.org](https://aimodels.org/download)
</div>

## 📖 Table of Contents

- [📝 Description](#-description)
- [📦 Installation](#-installation)
- [💻 Quickstart](#-quickstart)
- [📚 Documentation](#-documentation)
- [📜 License](#-license)

## 📝 Description

AI Model Manager CLI, it's like pip or npm - but for AI models!

For users, this allows easily managing your collection of AI models. It stores your models in a location that all of your AI enabled apps can access, so you don't need to worry about the huge files taking up so much space, or creating symlinks. Finally, no more having to hunt for a model and making sure you rename it and put it in the correct folder correctly. 

For developers, it means less code that you have to handle initializing your app and collecting all of the AI model resources needed. AI Model Manager also will provide security through checksum checks and pickle scanning.

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

## 📚 Documentation

[Documentation](https://docs.aimodels.org)

## 📜 License

[Apache License 2.0](./LICENSE.md)
