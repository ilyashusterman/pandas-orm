--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5
-- Dumped by pg_dump version 11.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	quickstart	collaborator
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add collaborator	7	add_collaborator
26	Can change collaborator	7	change_collaborator
27	Can delete collaborator	7	delete_collaborator
28	Can view collaborator	7	view_collaborator
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$390000$tAMgwJz9Sy3kOGaIZCu9UN$hrOhDb3CfjOHdKb3Py9p407adpuVJ4HBLqHZmolpass=	\N	t	admin			admin@example.com	t	t	2022-09-09 09:28:53.03444+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: collaborator; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.collaborator (id, name, first_name, last_name, email, profile_link, image_url) FROM stdin;
1	test	\N	bulk_create_sqlalchemy_returning_id	test@test.test	\N	\N
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2022-09-09 09:02:29.53037+00
2	auth	0001_initial	2022-09-09 09:02:29.593443+00
3	admin	0001_initial	2022-09-09 09:02:29.612321+00
4	admin	0002_logentry_remove_auto_add	2022-09-09 09:02:29.621103+00
5	admin	0003_logentry_add_action_flag_choices	2022-09-09 09:02:29.629764+00
6	contenttypes	0002_remove_content_type_name	2022-09-09 09:02:29.644728+00
7	auth	0002_alter_permission_name_max_length	2022-09-09 09:02:29.653217+00
8	auth	0003_alter_user_email_max_length	2022-09-09 09:02:29.662968+00
9	auth	0004_alter_user_username_opts	2022-09-09 09:02:29.670911+00
10	auth	0005_alter_user_last_login_null	2022-09-09 09:02:29.679319+00
11	auth	0006_require_contenttypes_0002	2022-09-09 09:02:29.682236+00
12	auth	0007_alter_validators_add_error_messages	2022-09-09 09:02:29.689919+00
13	auth	0008_alter_user_username_max_length	2022-09-09 09:02:29.699686+00
14	auth	0009_alter_user_last_name_max_length	2022-09-09 09:02:29.707842+00
15	auth	0010_alter_group_name_max_length	2022-09-09 09:02:29.716815+00
16	auth	0011_update_proxy_permissions	2022-09-09 09:02:29.725357+00
17	auth	0012_alter_user_first_name_max_length	2022-09-09 09:02:29.734316+00
18	sessions	0001_initial	2022-09-09 09:02:29.746354+00
19	quickstart	0001_create_collaborator	2022-09-09 09:59:11.159266+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: docker
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 28, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: collaborator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.collaborator_id_seq', 113, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 7, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: docker
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 19, true);


--
-- PostgreSQL database dump complete
--

