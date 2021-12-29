-- PROBLEM


Session id stepno endsecs

  1 1 10

  1 2 25

  1 3 45

  1 4 60

  2 1 70

  2 2 80

  2 3 95

  2 4 105



  create table steps_fb (sessionid int,stepno int, endsecs int )



  insert into steps_fb values(1,1,10);

insert into steps_fb values(1,2,25);

insert into steps_fb values(1,3,45);

insert into steps_fb values(1,4,60);

insert into steps_fb values(2,1,15);

insert into steps_fb values(2,2,20);

insert into steps_fb values(2,3,40);

insert into steps_fb values(2,4,60);



insert into steps_fb values(3,1,10);

insert into steps_fb values(3,2,22);

insert into steps_fb values(3,3,42);

insert into steps_fb values(3,4,50);



insert into steps_fb values(4,1,5);

insert into steps_fb values(4,2,12);

insert into steps_fb values(4,3,24);

insert into steps_fb values(4,4,36);



select * From steps_fb order by 1,2



select a.sessionid,a.stepno,a.endsecs,b.endsecs 

  from steps_fb a

       left join steps_fb b

           on a.stepno+1 = b.stepno

           and a.sessionid = b.sessionid

 order by 1,2
