CREATE TABLE tb_group_permission (
    group_id int REFERENCES tb_group (group_id) ON DELETE CASCADE,
    permission_id int REFERENCES tb_permission (permission_id) ON DELETE CASCADE,
    CONSTRAINT tb_group_permission_pkey PRIMARY KEY (group_id, permission_id)
)