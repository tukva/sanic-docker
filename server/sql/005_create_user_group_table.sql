CREATE TABLE tb_user_group (
    user_id int REFERENCES tb_user (user_id) ON DELETE CASCADE,
    group_id int REFERENCES tb_group (group_id) ON DELETE CASCADE,
    CONSTRAINT tb_user_group_pkey PRIMARY KEY (user_id, group_id)
)
