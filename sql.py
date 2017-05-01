schedule_group = '''
DECLARE @periodStart datetime = '{date} 00:00:00'
DECLARE @periodEnd datetime = '{date} 23:59:59'
DECLARE @group int = {id}
        SELECT 
            CONVERT(nvarchar(50), Rasp.[StartOn], 108) as StartOn,
                    Rasp.[StartTime], 
                    rasp.[group] as GroupName, 
                    rasp.[stream] as Stream, 
                    rasp.[subgroup] as Subgroup, 
                    Prep.[FIO] as 'Prepod', 
                    Disp.[Name] as 'Disciplina',
                    Vid.[Abbr] as 'Vid', 
                    Rasp.[Note], Aud.[Name] as 'Aud', 
                    Aud.[OID] as 'Aud_id', 
                    Para.[Number] as 'Para', 
                    SGr.[Name] as SubGroupName

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
            CONVERT(nvarchar(50), Rasp.[StartOn], 108) as StartOn, Rasp.[EndOn], Rasp.[StartTime], rasp.[group] as GroupName, Prep.[FIO] as 'Prepod', Prep.[Person] as 'Prepod_id',
            Disp.[Name] as 'Disciplina', Vid.[Abbr] as 'Vid', Rasp.[Note], Aud.[Name] as 'Aud', Aud.[OID] as 'Aud_id', Para.[Number] as 'Para', rasp.[stream] as Stream, rasp.[subgroup] as Subgroup, SGr.[Name] as SubGroupName
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
            #AND Rasp.Schedule IN (SELECT OID FROM Schedule WHERE FormOfEducation IN (4,6))

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

schedule_auditorium = '''
DECLARE @periodStart datetime = '{date} 00:00:00'
DECLARE @periodEnd datetime = '{date} 23:59:59'
DECLARE @aud int = {id}

        SELECT 
            CONVERT(nvarchar(50), Rasp.[StartOn], 108) as StartOn, Rasp.[EndOn], Rasp.[StartTime], rasp.[group] as GroupName, Prep.[FIO] as 'Prepod', Prep.[Person] as 'Prepod_id',
            Disp.[Name] as 'Disciplina', Vid.[Abbr] as 'Vid', Rasp.[Note], Aud.[Name] as 'Aud', Aud.[OID] as 'Aud_id', Para.[Number] as 'Para', rasp.[stream] as Stream, rasp.[subgroup] as Subgroup, SGr.[Name] as SubGroupName
            FROM 
            (SELECT [ContentOfSchedule].[StartOn] AS sd
            FROM [ContentOfSchedule] 
            WHERE [ContentOfSchedule].[StartOn] BETWEEN @periodStart AND @periodEnd
            GROUP BY [ContentOfSchedule].[StartOn]) Periods
            
            LEFT OUTER JOIN
            [ContentOfSchedule] Rasp 
            ON Periods.sd = Rasp.StartOn
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