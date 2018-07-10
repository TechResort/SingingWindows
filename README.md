# Singing Windows Documentation
TechResort's code for Devonshire Collective's Singing Windows installation.

This project works by using a Twitter bot to search for recent tweets using a certain (configurable) hashtag, and sends this tweet over to a Photon, a small internet of things device, which reads this and uses the contents of the tweet to control a display of lights.

## Hardware requirements:

* [Photon Internet of Things board](https://www.particle.io/)

* RGB LED matrix, controlled by Photon board

* microUSB power supply for Photon board

* Network connection for Photon board

## Software requirements:

* Twitter account and registered developer account

* Python twitter bot hosted and running online

* Light-controlling software on Photon board

