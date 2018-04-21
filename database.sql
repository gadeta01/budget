CREATE SEQUENCE user_id_seq;

CREATE TABLE public."User" (
    id integer NOT NULL DEFAULT NEXTVAL('user_id_seq'),
    LastName varchar(255),
    FirstName varchar(255),
    email character varying(120),
    password character varying(512) NOT NULL,
    token character varying(512),
    validated boolean,
    CONSTRAINT "user_pkey"  PRIMARY KEY (id)
);

CREATE SEQUENCE category_id_seq;

CREATE TABLE public."Category" (
  id integer NOT NULL DEFAULT NEXTVAL('category_id_seq'),
  title varchar(50),
  permonth integer NOT NULL,
  accumulated integer NOT NULL,
  userid integer NOT NULL,

  CONSTRAINT "category_pkey"  PRIMARY KEY (id),
  CONSTRAINT "category_user_fkey" FOREIGN KEY (userid)
        REFERENCES public."User" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION


    
);

CREATE SEQUENCE transaction_id_seq;

CREATE TABLE public."Transaction" (
    transactionid integer NOT NULL DEFAULT NEXTVAL('transaction_id_seq'),
    userid integer NOT NULL,
    category integer NOT NULL,
    amount integer NOT NULL,
    date date,
    payee varchar (50),

    CONSTRAINT "transaction_pkey"  PRIMARY KEY (transactionid),
    CONSTRAINT "transaction_user_fkey" FOREIGN KEY (userid)
        REFERENCES public."User" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT "transaction_category_fkey" FOREIGN KEY (category)
        REFERENCES public."Category" (id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);