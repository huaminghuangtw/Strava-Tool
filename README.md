Strava-Tool
===========

<p align="left">
<a href="https://github.com/huaminghuangtw/Strava-Tool"><img src="https://badges.frapsoft.com/os/v3/open-source.svg?v=103" alt="Open Source Love"></a><br/>
<a href="https://github.com/huaminghuangtw/Strava-Tool/releases"><img src="https://img.shields.io/github/v/release/huaminghuangtw/Strava-Tool.svg?display_name=tag&style=plastic&color=lightgrey"></a>
<a href="https://github.com/huaminghuangtw/Strava-Tool/tags"><img src="https://img.shields.io/github/v/tag/huaminghuangtw/Strava-Tool.svg?style=plastic&color=lightgrey"></a><br/> 
<a href="https://github.com/huaminghuangtw/Strava-Tool/stargazers"><img src="https://img.shields.io/github/stars/huaminghuangtw/Strava-Tool.svg?style=social"></a>
<a href="https://github.com/huaminghuangtw/Strava-Tool/fork"><img src="https://img.shields.io/github/forks/huaminghuangtw/Strava-Tool.svg?style=social"></a>
<a href="https://github.com/huaminghuangtw/Strava-Tool/issues"><img src="https://img.shields.io/github/issues/huaminghuangtw/Strava-Tool.svg?style=social&logo=github"></a>
<a href="https://github.com/huaminghuangtw/Strava-Tool/pulls"><img src="https://img.shields.io/github/issues-pr/huaminghuangtw/Strava-Tool.svg?style=social&logo=github"></a>
</p>

> A personal side project with Strava API using Python. 

<a href="https://www.strava.com/athletes/huaminghuang">
    <img src="figures&videos/follow-me-on-Strava.svg">
</a>

---

### Motivation
This project is my personal side project with Strava API.
The goal of this project is to analyze my training data for better future performance, as well as to **hone my Data Analysis & Visualization skills**.
The idea was originally coming from the fact that my increasing demands for uploading indoor cycling activity data to Strava, especially in the lockdown time of COVID-19.
I usually did indoor training with Zwift during the weekdays and long weekend group ride on the weekend.
When training indoors with Zwift, I used to also record my cycling workout with a bicycle computer, for more workout information like power zone, laps, time, etc.
This means there will be two generated files pointing to the same activity in the end. 
If you have authorized Zwift to connect with Strava beforehand, each of your virtual ride data will be AUTOMATICALLY synchronized to Strava.
That's really exciting and satisfying when you saw a Strava notification telling you that "Your activity is ready." after suffering on the saddle for hours.
(You know that feeling.😉)  

However, as an engineering graduate student and bike🚴 enthusiast, I decided to to take more control over the whole interaction process with Strava, 
in order to know what's happening under the hood.
Therefore, I disabled the connection between the two Apps, and started developing a toy StravaAutoUploader tool with Python as the starting point of this side project.
Hopefully it could be someday extended to have some advanced features like Golden Cheetah, TrainingPeaks, for analyzing, tracking, and predicting my performance on the bike!

<p align="center">
  <img width="300" height="460" src="https://user-images.githubusercontent.com/43208378/114391662-0a980000-9b98-11eb-9e49-9f48a532908f.JPG">
</p>

---

### Features (__just name a few, not completed yet__)
- Fixing and uploading workout (Ride, Virtual Ride, Run, Hike, etc.) activity files with the help of batch script automation using Task Scheduler (Windows)

https://user-images.githubusercontent.com/43208378/126695209-51a2c492-9b8d-4668-808d-801e813fe502.mp4

https://user-images.githubusercontent.com/43208378/126695221-0dcaaa7f-4b31-4093-ad5f-548504a6f335.mp4

- Analyzing workout data using Pandas package  
  e.g.,
    - yearly summary (similar to [Strava Year in Sport Data Report](https://blog.strava.com/press/yis2020/))  
    - How many workout activities I did per month/week in a year?  
      <img style="float: left" width="400" src="/figures&videos/Number_of_activities_per_month_in_2018.png">
    - How much time I spent on cycling activities per month/week in a year?
    - etc.
- Visualizing workout data using Seaborn and Matplotlib libraries as well as Tableau software   
  e.g.,
    - heatmap
    - etc.

---

### How to use the code
* [ ] Pipenv
* [ ] https://selenium-python.readthedocs.io/installation.html#drivers
* [ ] batch file
* [ ] auth
* [ ] config

---

### Good resources
- Getting started with Strava API:
  - [Getting Started With The Strava API: A Tutorial](https://medium.com/@annthurium/getting-started-with-the-strava-api-a-tutorial-f3909496cd2d)
  - [YouTube Playlist "Strava API for Beginners", by Fran Polignano](https://www.youtube.com/playlist?list=PLO6KswO64zVvcRyk0G0MAzh5oKMLb6rTW)
- Further development ideas: [Strava Labs](https://labs.strava.com/)
- [Strava API Developer Forum](https://groups.google.com/g/strava-api)

---

### Support the project
Whether you use this project, have learned something from it, or just like it, please consider supporting it by buying me a coffee or making one-time donations via PayPal, so I can dedicate more time on open-source projects like this. 💪🙃

<a href="https://www.buymeacoffee.com/huaming.huang" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="30" width="127" />
</a>
<a href="https://www.paypal.me/huaminghuang" target="_blank">
    <img src="https://ionicabizau.github.io/badges/paypal.svg" alt="paypal.me/huaminghuang" height="30" width="127" />
</a>

Thanks!:heart: and Cheers!:beers:

---

### Contact
If you have any question or suggestion, feel free to contact me at huaming.huang.tw@gmail.com. Contributions are also welcomed. Please open a [pull-request](https://github.com/huaminghuangtw/Strava-Tool/compare) or an [issue](https://github.com/huaminghuangtw/Strava-Tool/issues/new) in this repository.

---

### License

This project is licensed under the terms of [![MIT](https://img.shields.io/github/license/huaminghuangtw/Strava-Tool.svg?style=flat-square&label=License&colorB=black)](./LICENSE).