schedule_group = '''
DECLARE @periodStart datetime = '{date} 00:00:00'
DECLARE @periodEnd datetime = '{date} 23:59:59'
DECLARE @group int = {id}
        SELECT 
                Rasp.[StartTime] as start_time, 
                rasp.[group] as group_name, 
                rasp.[stream] as stream, 
                Prep.[FIO] as 'teacher', 
                Disp.[Name] as 'subject',
                Vid.[Abbr] as 'type', 
                Rasp.[Note] as note,
                Rasp.[Note], Aud.[Name] as 'classroom', 
                SGr.[Name] as subgroup_name

            FROM 
            
                (SELECT [ContentOfSchedule].[StartOn] AS sd
                FROM [ContentOfSchedule] 

                WHERE [ContentOfSchedule].[StartOn] BETWEEN @periodStart AND @periodEnd

                GROUP BY [ContentOfSchedule].[StartOn]) Periods

                LEFT OUTER JOIN
                    [ContentOfSchedule] Rasp 
                    ON Periods.sd = Rasp.StartOn
                    AND Rasp.Schedule IN (SELECT OID FROM Schedule WHERE Status = 0)
                    AND ((Rasp.[Group]=@group)
                OR (Rasp.[SubGroup]in
                (SELECT SGr.OID FROM [SubGroup] SGr WHERE SGr.[Group]=@group))
                OR 
                (Rasp.[stream]in
                (SELECT Sst.Stream FROM [StaffofStream] SSt WHERE Sst.[Group]=@group)))

                Left JOIN [Lecturer] as Prep
                ON rasp.[Lecturer] = Prep.[OID]

                Left JOIN [Discipline] as Disp
                ON Rasp.[Discipline]=Disp.[OID]

                Left JOIN [Auditorium] Aud
                ON Rasp.[Auditorium]=Aud.[OID]

                Left JOIN [ContentTableOfLesson] Para
                ON Rasp.[ContentTableOfLesson]=Para.[OID]

                Left JOIN [KindOfWork] Vid
                ON Rasp.[KindOfWork]=Vid.[OID]

                Left JOIN [SubGroup] Sgr
                ON Rasp.[SubGroup]=SGr.OID

                Left JOIN [Schedule] S
                ON Rasp.[Schedule]=S.[OID]
                
           

                WHERE StartOn IS NOT NULL
                order by start_time
'''

schedule_teacher = '''
DECLARE @periodStart datetime = '{date} 00:00:00'
DECLARE @periodEnd datetime = '{date} 23:59:59'
DECLARE @prep int = {id}

        SELECT 
            Rasp.[StartTime] start_time, 
            rasp.[group] as group_id, 
            [Group].Name as group_name,
            Prep.[FIO] as 'teacher', 
            Disp.[Name] as 'subject', 
            Vid.[Abbr] as 'type', 
            Rasp.[Note] as note, 
            Aud.[Name] as 'classroom', 
            rasp.[stream] as stream, 
            SGr.[Name] as subgroup_name
            
            FROM 
                (SELECT [ContentOfSchedule].[StartOn] AS sd
                FROM [ContentOfSchedule] 
                WHERE [ContentOfSchedule].[StartOn] BETWEEN @periodStart AND @periodEnd
                GROUP BY [ContentOfSchedule].[StartOn]) Periods
            
            LEFT OUTER JOIN
            [ContentOfSchedule] Rasp 
            ON Periods.sd = Rasp.StartOn
            AND Rasp.[Lecturer] IN (SELECT OID FROM [Lecturer] WHERE [Lecturer].Person = @prep)
            AND Rasp.Schedule IN (SELECT OID FROM Schedule WHERE Status = '0')


            Left JOIN [Lecturer] as Prep
            ON rasp.[Lecturer] = Prep.[OID]

            Left JOIN [Discipline] as Disp
            ON Rasp.[Discipline]=Disp.[OID]

            Left JOIN [Auditorium] Aud
            ON Rasp.[Auditorium]=Aud.[OID]

            Left JOIN [KindOfWork] Vid
            ON Rasp.[KindOfWork]=Vid.[OID]

            Left JOIN [SubGroup] Sgr
            ON Rasp.[SubGroup]=SGr.OID

            Left JOIN [Schedule] S
            ON Rasp.[Schedule]=S.[OID]
            
            left join [Group] on Rasp.[Group] = [Group].[OID]

            WHERE StartOn IS NOT NULL
            order by start_time
'''


schedule_classroom = '''
DECLARE @periodStart datetime = '{date} 00:00:00'
DECLARE @periodEnd datetime = '{date} 23:59:59'
DECLARE @aud int = {id}

        SELECT Distinct 
            Rasp.[StartTime] as start_time, 
            rasp.[group] as GroupName, 
            Prep.[FIO] as 'Prepod', 
            Prep.[Person] as 'Prepod_id',
            Disp.[Name] as 'Disciplina', 
            Vid.[Abbr] as 'Vid', 
            Rasp.[Note], 
            Aud.[Name] as 'Aud', 
            Aud.[OID] as 'Aud_id', 
            Para.[Number] as 'Para', 
            rasp.[stream] as Stream, 
            rasp.[subgroup] as Subgroup, 
            SGr.[Name] as SubGroupName
                FROM 
                
                (SELECT [ContentOfSchedule].[StartOn] AS sd
                FROM [ContentOfSchedule] 
                WHERE [ContentOfSchedule].[StartOn] BETWEEN @periodStart AND @periodEnd) Periods
            
            LEFT OUTER JOIN
            [ContentOfSchedule] Rasp ON Periods.sd = Rasp.StartOn
            AND Rasp.[Auditorium] IN (SELECT OID FROM [Auditorium] WHERE [Auditorium].OID = @aud)
            AND Rasp.Schedule IN (SELECT OID FROM Schedule WHERE Status = '0')

            Left JOIN [Lecturer] as Prep
            ON rasp.[Lecturer] = Prep.[OID]

            Left JOIN [Discipline] as Disp
            ON Rasp.[Discipline]=Disp.[OID]

            Left JOIN [Auditorium] Aud
            ON Rasp.[Auditorium]=Aud.[OID]

            Left JOIN [ContentTableOfLesson] Para
            ON Rasp.[ContentTableOfLesson]=Para.[OID]

            Left JOIN [KindOfWork] Vid
            ON Rasp.[KindOfWork]=Vid.[OID]

            Left JOIN [SubGroup] Sgr
            ON Rasp.[SubGroup]=SGr.OID

            Left JOIN [Schedule] S
            ON Rasp.[Schedule]=S.[OID]

            WHERE StartOn IS NOT NULL
            order by start_time
'''


lecturers_stream = '''
    SELECT DISTINCT [Group].[Name] as 'group'
    FROM [Group] , [StaffOfStream] Str
    where Str.[Stream]={stream_id} and Str.[Group]=[Group].[OID]

'''


select_groups = '''
select distinct gr.Name as group_name, gr.group_id
from
  (
  SELECT Distinct gr.OID as group_id, gr.Name
  from [Group] gr, [SubGroup] sgr, [ContentOfSchedule] Rasp, [Schedule] S
  where
  gr.[OID] = sgr.[Group] and sgr.[OID] = rasp.SubGroup
  and Rasp.Schedule=S.OID and S.[Status]='0'
  AND Rasp.Schedule IN (SELECT OID FROM Schedule WHERE FormOfEducation IN ({0}))

  UNION all
  SELECT Distinct gr.OID as group_id, gr.Name
  from [Group] gr, [ContentOfSchedule] Rasp, [Schedule] S
  where
  gr.[OID] = rasp.[Group] and Rasp.Schedule=S.OID and S.[Status]='0'
  AND Rasp.Schedule IN (SELECT OID FROM Schedule WHERE FormOfEducation IN ({0}))

  UNION all
  SELECT Distinct gr.OID as group_id, gr.Name
  from [Group] gr, [StaffOfStream] str, [ContentOfSchedule] Rasp, [Schedule] S
  where
  gr.[OID] = str.[Group] and str.[Stream] = rasp.Stream and Rasp.Schedule=S.OID
  and S.[Status]='0' AND Rasp.Schedule IN (SELECT OID FROM Schedule WHERE FormOfEducation IN ({0}))

  ) as gr'''


select_group_name = '''
select Name from [Group] Where [Group].OID ={id}
'''


select_all_teachers = '''
SELECT DISTINCT Prep.[Person] as teacher_id,
(CASE
WHEN Prep.[Note] is Null
THEN Prep.[FIO]
ELSE
case
WHEN Prep.[Note] is not Null
Then Prep.[Note]
end
END) as 'fullname', FIO as 'shortname'

FROM [ContentOfSchedule] Rasp, [Lecturer] Prep, [Schedule] S
where Rasp.[Lecturer]=Prep.[OID] and Rasp.Schedule=S.OID and S.[Status]='0'
ORDER BY FIO
'''


select_classrooms = '''
SELECT DISTINCT Cast(Bild.[Name] AS INT) as Build, Aud.[Name], Aud.OID as classroom_id,

(CASE
WHEN Bild.[Name] = '0'
THEN 'Главный учебный корпус'
ELSE
case
WHEN Bild.[Name] = '100'
Then 'Дополнительно'
ELSE
case
WHEN Bild.[Name] < '99'
Then 'Учебный корпус №' + Bild.[Name]
END
end
END) as Korpus

FROM [Auditorium] Aud

Left JOIN Building Bild
ON Aud.Building = Bild.OID

Group by Bild.[Name], Aud.[Name], Aud.OID

ORDER BY Cast(Bild.[Name] AS INT), Aud.[Name]
'''


groups_course = """
select Course from [Group] 
where OID ={0}
"""


