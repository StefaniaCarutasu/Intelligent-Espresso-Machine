<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">Intelligent Espresso Machine</h3>

  <p align="center">
    Russia's greatest espresso machine.
    <br />
    <a href="https://github.com/StefaniaCarutasu/Intelligent-Espresso-Machine"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot](https://user-images.githubusercontent.com/62221313/151992718-1631c628-1cfa-4602-8fdb-04ef52ebabee.png)

Did you ever wish to have the perfect coffee just a button press away? In that case, your wish is about to come true with Rasputin. Our intelligent coffee machine is designed to suit all of your needs and even some you never knew you had.

The machine comes with a variety of coffee recipes which can be personalized by choosing the roast level of the coffee (including the option for decaffeinated) and whether to add syrup or not to the beverage. It can also make suggestions according to the outside temperature or the user's blood pressure level, which comes in handy for those with heart problems who still want to enjoy a nice cup of coffee.

Each user has a different profile where he can set his favorite beverage which from that moment on can be made with just a button press. Users can also program the machine to make them a coffee at any given time during the day. No more running around in the morning to prepare your coffee. Let Rasputin take care of it and enjoy waking up to the smell of fresh coffee.

Our machine is constantly checking its internal state, letting you know when its running low on coffee, milk or syrup. It also checks to see if everything is working normally to let you know if it needs any type of mentenace.

In other words, Rasputin combines the basic requirments of a coffee machine with some 21st century features to elevate your coffee making experience.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [OpenWeatherMap](https://openweathermap.org/api)
* [Mqtt](https://mqtt.org/)
* [Werkzeug](https://werkzeug.palletsprojects.com/en/2.0.x/)
* [WTForms](https://wtforms.readthedocs.io/en/3.0.x/)
* [Mosquitto](https://mosquitto.org/)
* [Bootstrap](https://getbootstrap.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

You need to have python 3, pip 3 and mosquitto already installed on your machine.

### Installation

1. cd into this project  

2. Install venv if not already installed:  
`pip install virtualenv`
  
3. Create an environment:  
macOS/Linux:
`python3 -m venv ./`  
Windows:
`python -m venv venv`  

4. Activate environment  
macOS/Linux:
`source venv/bin/activate`  
Windows:
`venv\Scripts\activate`

5. Install libraries:  
`pip install -r requirements.txt`

6. Set name value for rasputin:  
macOS/Linux:
`export FLASK_APP=rasputin`  
CMD:
`set FLASK_APP=rasputin`  
PowerShell:
`$env:FLASK_APP = "rasputin"`  

7. Set environment value for development:  
macOS/Linux:
`export FLASK_ENV=development`  
CMD:
`set FLASK_ENV=development`  
PowerShell:
`$env:FLASK_ENV = "development"`  

8. Initialize (or reinitialize) database:  
`flask init-db`

9. Populate database:  
`flask populate-coffee-table`  
`flask populate-machine-state`

10. Run:  
Http:
`flask run` or `python -m flask run`  
Mqtt:  
CMD PROMPT 1:
`cd mosquitto`
`mosquitto -v`  
CMD PROMPT 2:
`python main.py`  
CMD PROMP 3:
`cd rasputin`
`python mqtt-comms-sub.py`  

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Register
- [x] Log in
- [x] Log out
- [x] Make coffee
- [x] Refill coffee
- [x] Refill milk
- [x] Refill syrup
- [x] Edit profile
   - [x] Change preference
   - [x] Add programmed coffee
   - [x] Delete programmed coffee
- [x] Coffee suggestions     
    - [x] Based on temperature
    - [x] Based on blood pressure

![image](https://user-images.githubusercontent.com/62221313/152016584-729ea77c-8e9e-44f1-90f2-2aa2bda047b4.png)

![image](![image](https://user-images.githubusercontent.com/62119841/152068259-c82035fc-e7fd-4254-9d0c-7415f9d98c2b.png)
)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/StefaniaCarutasu/Intelligent-Espresso-Machine](https://github.com/StefaniaCarutasu/Intelligent-Espresso-Machine)

On this project worked:
- Agha Mara
- Carutasu Stefania
- Costrun Larisa
- Dudau Claudia
- Nicolescu Madalina

<p align="right">(<a href="#top">back to top</a>)</p>
