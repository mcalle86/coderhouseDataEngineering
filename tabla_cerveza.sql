CREATE TABLE marcocalle86_coderhouse.cerveza (
   id int not null PRIMARY KEY
   ,marca varchar(40) NULL
   ,nombre varchar(40) NULL
   ,estilo varchar(40) NULL
   ,lupulo varchar(40) NULL
   ,levadura varchar(40)
   ,malta varchar(30)
   ,amargor int
   ,alcohol numeric(4,2)
   ,blg numeric(4,2) null
)SORTKEY(marca,estilo);