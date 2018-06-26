# **Error Propagation tool**

Designed to find the error propagation equation and sample calculation. It then outputs result in latex form to copy paste into report. 

## **Prerequisites**

This small python3 program makes heavy use of the **PyQt5** and **Sympy** framework.
You can install them by running.

 ```bash
 pip install pyqt5
 pip install sympy
 ```

## **Usage**

After ensuring that you`ve installed all the prerequisites mentioned above. Launch the application with,

```bash
python gui.py
```

 The window presented in figure 1 will pop up. Note that preloaded equation is for test purposes you can edit the source if you wish to get rid of it, **gui.py, line 63.**

![Figure 1](articles/mainWindow.PNG)

* **Equation** : Expression on which you wish to error propagate.
* **Variables**: Specify differentiable variables, constants should not be included.

Hitting the submit button launches the sample calculation window presented in Figure 2. Sample calculation variables includes both constants and variables. As seen by the example used. The **symbol a** was not specified as a varibles but still showed up in the sample calculation window.

![Figure 2](articles/varWindow.PNG)

Hitting submit on the sample calculation window populates the latex Output box in the mainwindow as seen in Figure 3.
 
 ![Figure 2](articles/mainWindowFinal.PNG)
 
View the output on any latex interpreter.