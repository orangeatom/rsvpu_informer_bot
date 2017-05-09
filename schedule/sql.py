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
            Rasp.[Note], 
            Aud.[Name] as 'classroom', 
            rasp.[stream] as stream, 
            SGr.[Name] as subgruop_name
            
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
            
            left join [Group] on Sgr.[Group] = [Group].[OID]

            WHERE StartOn IS NOT NULL
'''

schedule_auditorium = '''
DECLARE @periodStart datetime = '{date} 00:00:00'
DECLARE @periodEnd datetime = '{date} 23:59:59'
DECLARE @aud int = {id}

        SELECT Distinct 
            CONVERT(nvarchar(50), Rasp.[StartOn], 108) as StartOn, 
            Rasp.[EndOn], 
            Rasp.[StartTime], 
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
'''


lecturers_stream = '''
    SELECT DISTINCT [Group].[Name] as 'Group', 
                    [Group].[OID]
    FROM [Group] , [StaffOfStream] Str
    where Str.[Stream]={stream_id} and Str.[Group]=[Group].[OID]

'''


select_group = '''
Select Name,OID from [Group] 
inner JOIN Schedule on 
'''


select_group_name = '''
select Name from [Group] Where [Group].OID ={id}
'''

select_all_teachers = '''select Name from [Lecturer]'''

selection_teachers_by_name = '''
select Name from [Lecturer] where lower(Name) like '%{0}%'''