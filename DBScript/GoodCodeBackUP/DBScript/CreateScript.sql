select * from battery;
select * from datecalendar; 
select * from callstate; 
select * from network; 
select * from wakelockinformation;

-- INSERT INTO callstate (call_state ,timestamp ,probe_transmit_mode) 
--                            VALUES ('A','B','C')

-- create table public."datecalendar" (day_of_year integer,month integer,dst_offset integer,day_of_month integer,week_of_month integer,probe_transmit_mode integer,day_of_week_in_month integer,week_of_year integer,hour_of_day integer,
-- 								timestamp integer,minute integer,day_of_week integer);

-- DROP TABLE  wakelockinformation;
-- create table wakelockinformation (bright_count text,dim_locks text, partial_count text,timestamp text, full_locks CHAR(50), bright_locks CHAR(50), partial_locks CHAR(50), dim_count text, probe_transmit_mode text , 
-- 								  full_count text);

-- DROP TABLE  network;
-- create table network (interface_name CHAR(50), interface_display CHAR(10), 
-- hostname CHAR(100), timestamp integer, ip_address CHAR(100),probe_transmit_mode TEXT);

-- drop table battery
-- create table battery (id number,icon_small text,invalid_charger text,level text,
-- health text,scale text,priority CHAR(10),technology CHAR(10), charge_counter text,
-- max_charging_current text,probe_transmit_mode text,voltage text,timestamp text,temperature text,
-- max_charging_voltage text,present CHAR(10),battery_low CHAR(10),plugged text,seq status text);



delete from battery;
delete from datecalendar; 
delete from callstate; 
delete from network; 
delete from wakelockinformation;

select * from location;
select * from sunrisesunsetfeature;
select * from wifiaccesspoints;
select * from wakelockinformation;
select * from battery;
select * from network;
select * from datecalendar;
select * from callstate;
select distinct userhash from callstate;

-- "34237272481aa6a02ea94799695a6983"

--insert into callstate values (26,'34237272481aa6a02ea94799695a6983','Ringing','1551905360','0')
-- insert into battery (level,timestamp,userhash) values (30,'1551905360','34237272481aa6a02ea94799695a6983')

-- update battery set level = 60,timestamp='1551905360' where userhash = '34237272481aa6a02ea94799695a6982'

-- "1551905360"


-- truncate table network;
-- truncate table datecalendar;

-- truncate table callstate;





