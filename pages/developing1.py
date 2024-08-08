import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container

from src2.navigation import navigation

navigation()


script = """
    <style>
        .main{
            font-family: sans-serif;
            background-color: #20d2df;
        }
        
        .container{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        
        .battery-status{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 20px 10px rgba(202,202,202,0.2);
        }
        
        .battery-level{
            position: relative;
            width: 150px;
            height: 60px;
            background-color: #e4e4e4;
            border-radius: 30px;
            overflow: hidden;
        }
        
        .battery-fill{
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            background-color: #00e09d;
            transition: width 0.5s ease;
        }
        
        .battery-percentage{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24px;
            font-weight: bold;
            color: #f5f5f5;
        }
        
        .battery-status-text{
            margin-top: 10px;
            font-size: 20px;
            font-weight: bold;
            color: #a8a8a8;
        }
    </style>


    <div class="main">
          <div class="container">
              <div class="battery-status">
                <div class="battery-level">
                  <div class="battery-fill"></div>
                  <span class="battery-percentage">100%</span>
                </div>
                <div class="battery-status-text">Plugged In</div>
              </div>
          </div>
          <script src="script.js"></script>
    </div>

    

    <script>
        navigator.getBattery().then(function(battery)
            {
                updateBatteryStatus(battery);
                battery.addEventListener('levelchange',function(){
                    updateBatteryStatus(battery);
                });
                battery.addEventListener('chargingchange', function(){
                    updateBatteryStatus(battery);
                });
            });
            
        function updateBatteryStatus(battery) {
            var batteryFill = document.querySelector(".battery-fill");
            var batteryPercentage = document.querySelector(".battery-percentage");
            var batteryStatusText = document.querySelector(".battery-status-text");
        
            var fillWidth = Math.round(battery.level * 100) + "%";
            batteryFill.style.width = fillWidth;
            batteryPercentage.innerHTML = fillWidth;
        
            if (battery.charging){
                batteryStatusText.innerHTML = "Now is Charging";
            } else {
                batteryStatusText.innerHTML = "Not Charging";
            }
        }
    </script>

"""


components.html(
    script,
    height=1000,
)
