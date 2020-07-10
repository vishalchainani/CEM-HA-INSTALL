
[issue description]
https://bugs.launchpad.net/kolla-ansible/+bug/1712087
https://bugs.launchpad.net/kolla-ansible/+bug/1712087/comments/5



[error log]
2019-09-30 10:58:50 140465114863808 [ERROR] WSREP: failed to open gcomm backend connection: 110: failed to reach primary view: 110 (Connection timed out)
         at gcomm/src/pc.cpp:connect():162
2019-09-30 10:58:50 140465114863808 [ERROR] WSREP: gcs/src/gcs_core.cpp:gcs_core_open():208: Failed to open backend connection: -110 (Connectiontimed out)
2019-09-30 10:58:50 140465114863808 [ERROR] WSREP: gcs/src/gcs.cpp:gcs_open():1380: Failed to open channel 'openstack' at 'gcomm://172.27.14.127:4567,172.27.14.149:4567,172.27.14.128:4567': -110 (Connection timed out)
2019-09-30 10:58:50 140465114863808 [ERROR] WSREP: gcs connect failed: Connection timed out
2019-09-30 10:58:50 140465114863808 [ERROR] WSREP: wsrep::connect(gcomm://172.27.14.127:4567,172.27.14.149:4567,172.27.14.128:4567) failed: 7
2019-09-30 10:58:50 140465114863808 [ERROR] Aborting



[procedure]

check seqno (for me, every node has -1)
# cat /var/lib/docker/volumes/mariadb/_data/grastate.dat

add this to that file
--
safe_to_bootstrap: 0
--

type this command
--
docker run --net host --name mariadbbootstrap -v /etc/localtime:/etc/localtime:ro -v kolla_logs:/var/log/kolla/ -v mariadb:/var/lib/mysql -v /etc/kolla/mariadb/:/var/lib/kolla/config_files/:ro --restart on-failure:10 --env KOLLA_CONFIG_STRATEGY=COPY_ALWAYS --env BOOTSTRAP_ARGS='--wsrep-new-cluster' kolla/centos-binary-mariadb:queens
--

bootstrap container will be UP
--
++ chmod 755 /var/log/kolla/mariadb
++ [[ -n '' ]]
++ [[ -n 0 ]]
++ ARGS=--wsrep-new-cluster
+ echo 'Running command: '\''/usr/bin/mysqld_safe --wsrep-new-cluster'\'''
+ exec /usr/bin/mysqld_safe --wsrep-new-cluster
Running command: '/usr/bin/mysqld_safe --wsrep-new-cluster'
191001 06:43:36 mysqld_safe Logging to '/var/log/kolla/mariadb/mariadb.log'.
191001 06:43:36 mysqld_safe Starting mysqld daemon with databases from /var/lib/mysql/
191001 06:43:36 mysqld_safe WSREP: Running position recovery with --log_error='/var/lib/mysql//wsrep_recovery.hbbvNp' --pid-file='/var/lib/mysql//ip-172-31-0-141.ap-northeast-1.compute.internal-recover.pid'
191001 06:43:43 mysqld_safe WSREP: Recovered position c580b2fe-e40c-11e9-aa9a-bb75bc584842:7622
--


Two mariadb become UP

--
[root@ip-172-31-13-186 ~]# tail -f /var/lib/docker/volumes/kolla_logs/_data/mariadb/mariadb.log
2019-10-01  6:47:28 140586460646144 [Note] WSREP: Provider resumed.
2019-10-01  6:47:28 140591048414976 [Note] WSREP: 1.0 (ip-172-31-13-186): State transfer to 0.0 (ip-172-31-15-177) complete.
2019-10-01  6:47:28 140591048414976 [Note] WSREP: Shifting DONOR/DESYNCED -> JOINED (TO: 7717)
2019-10-01  6:47:28 140591048414976 [Note] WSREP: Member 1.0 (ip-172-31-13-186) synced with group.
2019-10-01  6:47:28 140591048414976 [Note] WSREP: Shifting JOINED -> SYNCED (TO: 7717)
2019-10-01  6:47:28 140590990162688 [Note] WSREP: Synchronized with group, ready for connections
WSREP_SST: [INFO] Total time on donor: 0 seconds (20191001 06:47:28.360)
WSREP_SST: [INFO] Cleaning up temporary directories (20191001 06:47:28.369)
2019-10-01  6:47:33 140591048414976 [Note] WSREP: 0.0 (ip-172-31-15-177): State transfer from 1.0 (ip-172-31-13-186) complete.
2019-10-01  6:47:33 140591048414976 [Note] WSREP: Member 0.0 (ip-172-31-15-177) synced with group.

[root@ip-172-31-15-177 ~]# tail -f /var/lib/docker/volumes/kolla_logs/_data/mariadb/mariadb.log
2019-10-01  6:47:33 140079655401664 [Note] Server socket created on IP: '172.31.15.177'.
2019-10-01  6:47:33 140079655401664 [Note] WSREP: Signalling provider to continue.
2019-10-01  6:47:33 140079655401664 [Note] WSREP: SST received: c580b2fe-e40c-11e9-aa9a-bb75bc584842:7717
2019-10-01  6:47:33 140079309756160 [Note] WSREP: 0.0 (ip-172-31-15-177): State transfer from 1.0 (ip-172-31-13-186) complete.
2019-10-01  6:47:33 140079309756160 [Note] WSREP: Shifting JOINER -> JOINED (TO: 7727)
2019-10-01  6:47:33 140079309756160 [Note] WSREP: Member 0.0 (ip-172-31-15-177) synced with group.
2019-10-01  6:47:33 140079309756160 [Note] WSREP: Shifting JOINED -> SYNCED (TO: 7727)
2019-10-01  6:47:33 140079655401664 [Note] /usr/libexec/mysqld: ready for connections.
Version: '10.1.20-MariaDB'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  MariaDB Server
2019-10-01  6:47:33 140074936666880 [Note] WSREP: Synchronized with group, ready for connections
--


remove bootstrap mariadb

--
[root@ip-172-31-0-141 ~]# docker stop mariadbbootstrap
mariadbbootstrap
[root@ip-172-31-0-141 ~]# docker rm mariadbbootstrap
mariadbbootstrap

docker start mariadb
--


[root@ip-172-31-0-141 ~]# tail -f /var/lib/docker/volumes/kolla_logs/_data/mariadb/mariadb.log                                                                                                    2019-10-01  6:51:52 140510603447040 [Note] WSREP: Receiving IST: 277 writesets, seqnos 7967-8244
2019-10-01  6:51:52 140510604953792 [Note] /usr/libexec/mysqld: ready for connections.
Version: '10.1.20-MariaDB'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  MariaDB Server
2019-10-01  6:51:52 140510475785984 [Note] WSREP: (488cbcfb, 'tcp://172.31.0.141:4567') turning message relay requesting off
2019-10-01  6:51:52 140510603447040 [Note] WSREP: IST received: c580b2fe-e40c-11e9-aa9a-bb75bc584842:8244
2019-10-01  6:51:52 140510257735424 [Note] WSREP: 2.0 (ip-172-31-0-141): State transfer from 1.0 (ip-172-31-13-186) complete.
2019-10-01  6:51:52 140510257735424 [Note] WSREP: Shifting JOINER -> JOINED (TO: 8250)
2019-10-01  6:51:52 140510257735424 [Note] WSREP: Member 2.0 (ip-172-31-0-141) synced with group.
2019-10-01  6:51:52 140510257735424 [Note] WSREP: Shifting JOINED -> SYNCED (TO: 8250)
2019-10-01  6:51:52 140510603447040 [Note] WSREP: Synchronized with group, ready for connections


ueolla-toolbox)[ansible@ip-172-31-0-141 /var/tmp]$ openstack token issu
+------------+----------------------------------+
| Field      | Value                            |
+------------+----------------------------------+
| expires    | 2019-10-01T07:52:37+0000         |
| id         | a11abb1c9b4b4d839bf692c815cfbc4a |
| project_id | b7c262ebc8274ca682785978b776c4c1 |
| user_id    | 3962147ff2a94a2ba264769871b0999a |
+------------+----------------------------------+
(kolla-toolbox)[ansible@ip-172-31-0-141 /var/tmp]$

