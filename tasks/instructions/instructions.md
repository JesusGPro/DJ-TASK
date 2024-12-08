# Instructions for Using the Application

## Introduction
This document provides instructions on how to use the Budget Application.

This app creates a budget for a project. The chapters or this budger are called workpackages. In every workpackage we include works. A work is a task x a quantity. A task is made up of components. The final output is the total budget quantity, but also we will know the breakdown for every workpackage. The quantity can also be brokendown.

## Installation
1. You have to receive a user and a password to work with the app.
2. Introduce this link: https://jesusgp.pythonanywhere.com/
3. You are ready to roll.

## Usage
### Starting the Application
You will see this page:

![alt text](/static/instructions/image-0.png)

Then you have to log in:
![alt text](/static/instructions/image-1.png)

Then you must create or select a project, without it, there is not much to do.

![alt text](/static/instructions/image-2.png)
### Creating a project:
![alt text](/static/instructions/image-4.png)


### Selecting a project:
![alt text](/static/instructions/image-3.png)

### Application's principles
First of all we have to create WorkPackages. These are the chapters of the budget. In each chapter we will introduce works. These works are link with a chapter, to be introduced by the user. The work is made up of a Task, that will include a code, a  name, a project(foreignkey link to Project) a unit, a price, a currency and several component(components are related to material, machinery and menpower), and a quantity introduced by the user, the result will be a figure: task price x quantity. At the end the grand total will be the sum of all this task prices x quantities.
Summarizing:
    • WorkPackages (chapters of the budget)
    • Works (linked to a WorkPackage)
    • Tasks (part of a Work)
    • Components(parts of Task)
Each Task has several attributes:
    • Code
    • Name
    • Project (foreign key link to Project)
    • Unit
    • Price
    • Currency
    • Components (many-to-many link to Price)
    • Quantity (introduced by the user)

Task are created independently, not linked to any WorkPackage, also a Task, might be used in differnte WorkPackages, even in different Projects of the same user. 

To introduce a work, first we have to select a workpackage.

### Creating WorkPackages
![alt text](/static/instructions/image-5.png)

![alt text](/static/instructions/image-6.png)

**It is very important to introduce the levels as indicator of hierarchy, so, if our project will have 5 levels, the first one will be 10000, the rest levels starting with 1, such as 11000 will be children**. For example:

![alt text](/static/instructions/image-7.png)

### Creating Tasks
Click in the menu Task and create a new one.
For the code will follow the CSI criteria, so if we have a subdivision 31 71 00 - Tunnel excavation, the task will have the code 317101 and the name will be: Excavation with TBM type EPM, internal diameter 9.45m and excavation diameter 10.38m from 0+056 to 9+111. 

![alt text](/static/instructions/image-8.png)

### Adding Components
Clicking in the View/Edit button:

![alt text](/static/instructions/image-9.png)

You can add any component. If you are starting you need to create first. You can do at the same time opening a second window, creating in this second window and adding in the initial one.

![alt text](/static/instructions/image-10.png)

We have created a price that is related to 377100 so we add a number and a "Q" related to machinery. If it is a material we can add a "M" and a "P" for menpower and so on.

When adding the component we have to include the quantity(only 6 decimal positions allowed). In this case we need two, one for mobilization and another one for demobilization. You cand add the prices in EUR, USD or SAR. The it will be converted to the project's currency. To update the currency rates got to the "Currency" menu in the navigation bar.

![alt text](/static/instructions/image-11.png)

### Creating Reports
#### 1.-WorkPackge Report
You can create reports of any Work Package, if you click here you will get a menu page, and the you would be able to create a view, generate a pdf, generate a csv with and without measurements, with measurements you have also available a xlsx (excel) report.

![alt text](/static/instructions/image-12.png)

An example of a view with measurements:
![alt text](/static/instructions/image-13.png)

#### 2.-WorkPackge Report Div level in CSI budget

If you are working with CSI MasterFormat, you have a Project and then you have 3 or 4 levels, for examaple:
Division 03 - Concrete
Level 1 - 03 20 00 Concrete Reinforcing
Level 2 - 03 21 00 Reinforcing Steel
Level 3 - 03 21 13 Galvanized Reinforcing Steel
Level 4 - 03 21 13.01 Galvanized Reinforcing Steel for foundations

After level 2 or 3 we will have the tasks or items.

In Line 7 tender example, the Work Packages with tasks will be the one with 3 figures, for example WP 3.1.6: Bridge/Viaduct, son the code for this Work Package will be 3 followed by 1 and then followed by 06, because we will have in this level more than 10, and then followed by 000, so the final level number will be "3106000".

After that we will create Division 03 - Concrete, that will have the level "3106030", then we can add Division 05 - Metals, that will have the level "3106050", the we will add, Division 31 - Earthworks, that will have the level "3106310". All this Divisions will have as parents 3106000.








