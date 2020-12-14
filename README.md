# Coupler

Coupler (`cpl` in the terminal) is an experimental tool to replace the standard terminal workflow of `commands | seperated | by | pipes` by injecting a pipe "coupler" that replaces the traditional shell commands with an interactive scripting environment. The purpose is to replace all the intermediary commands with 1 shell script `input | cpl | output`.
Currently only python is supported as a scripting language, in fact there is no way to configure any aspect of Coupler at this time. This project was written in one inspiration filled weekend and as such does not support [everything I want](#vision) and the code could rightfully be called spaghetti by someone other than me.
Coupler is primarily an experiment for myself in alternative ways of interacting with the shell, I don't know if it will be of use to anyone else but I think it's a neat idea, and hope you do to0!

# Example
A fake example to demonstrate the basic behaviour.
<p align="center"><img src="/images/demo.gif?raw=true"/></p>

# Installation
Coupler uses [poetry](https://python-poetry.org/) for packaging and dependency management, the simplest way to install would simply be:
```
git clone https://github.com/CalebJohn/shell-coupler.git
pip install shell-coupler/
```

# Usage
Scripts created with Coupler are simply python scripts that operate on 1 provided variable `inpipe` (if you have a better variable name, I'm definitely open to suggestions). There is no magic going on by capturing io or anything like that, just a plain ol' python script getting executed on every keypress :slight_smile:.

# Vision
In it's current state, Coupler is just a proof-of-concept for the idea of replacing a series of shell commands with an interactive scripting environment. I've already started using it for some simple tasks and it performs well, but I don't imagine it's foolproof.

If I find that I'm relying on Coupler, I'll probably start implementing some of the below.
- [ ] Enable the `Tab` key in the editor (didn't I say this was proof-of-concept?)
- [ ] Add a configuration system
	- [ ] Support custom scripting languages
	- [ ] Support custom styles
- [ ] Add an external editor option

