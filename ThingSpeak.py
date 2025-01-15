% Read temperature data from a ThingSpeak channel over the past 24 hours 
% to calculate the high and low temperatures and write to another channel. 

% Channel ID to read data from 
readChannelID = xxxxxx; 
% Temperature Field ID 
TemperatureFieldID = 1; 
   
% Channel Read API Key   
% If your channel is private, then enter the read API Key between the '' below: 
readAPIKey = 'xxxxxxxxxxxx'; 
   
[tempF,timeStamp] = thingSpeakRead(readChannelID,'Fields',TemperatureFieldID, ...
                                                'numDays',1,'ReadKey',readAPIKey); 
   
% Calculate the maximum and minimum temperatures 
[maxTempF,maxTempIndex] = max(tempF); 
[minTempF,minTempIndex] = min(tempF); 
   
% Select the timestamps at which the maximum and minimum temperatures were measured
timeMaxTemp = timeStamp(maxTempIndex); 
timeMinTemp = timeStamp(minTempIndex); 
   
display(maxTempF,'Maximum Temperature for the past 24 hours is'); 
display(minTempF,'Minimum Temperature for the past 24 hours is');    
   
% Replace the [] with channel ID to write data to: 
writeChannelID = xxxxxx; 
% Enter the Write API Key between the '' below: 
writeAPIKey = 'xxxxxxxxxxxx'; 
