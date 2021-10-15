CUSTOM_TABLE_HEADERS = {
    "requests" : ["id","timestamp","user_id","course_id", "quiz_id", "discussion_id","conversation_id","assignment_id","url","user_agent"],
    "user_dim" : ['id', 'canvas_id', 'root_account_id','name','time_zone','created_at','visibility','school_name','school_position','gender', 'locale','public','birthdate','country_code','workflow_state','sortable_name', 'global_canvas_id']
}

USECOLS = {
    "requests" : [0,1,5,6,9,10,11,12,13,14,22,27]
}

TRUNCATE_TABLES_EXCEPTION = ["requests"]
CANVAS_TABLES = [
            "account_dim",
            "assignment_dim",
            "assignment_fact",
            "assignment_group_dim",
            "assignment_group_fact",
            "assignment_group_rule_dim",
            "assignment_group_score_dim",
            "assignment_group_score_fact",
            "assignment_override_dim",
            "assignment_override_fact",
            "assignment_override_user_dim",
            "assignment_override_user_fact",
            "assignment_override_user_rollup_fact",
            "assignment_rule_dim",
            "communication_channel_dim",
            "communication_channel_fact",
            "conference_dim",
            "conference_fact",
            "conference_participant_dim",
            "conference_participant_fact",
            "conversation_dim",
            "conversation_message_dim",
            "conversation_message_participant_fact",
            "course_dim",
            "course_score_dim",
            "course_score_fact",
            "course_section_dim",
            "course_ui_canvas_navigation_dim",
            "course_ui_navigation_item_dim",
            "course_ui_navigation_item_fact",
            "discussion_entry_dim",
            "discussion_entry_fact",
            "discussion_topic_dim",
            "discussion_topic_fact",
            "enrollment_dim",
            "enrollment_fact",
            "enrollment_rollup_dim",
            "enrollment_term_dim",
            "external_tool_activation_dim",
            "external_tool_activation_fact",
            "file_dim",
            "file_fact",
            "group_dim",
            "group_fact",
            "group_membership_dim",
            "group_membership_fact",
            "learning_outcome_dim",
            "learning_outcome_fact",
            "learning_outcome_group_association_fact",
            "learning_outcome_group_dim",
            "learning_outcome_group_fact",
            "learning_outcome_question_result_dim",
            "learning_outcome_question_result_fact",
            "learning_outcome_result_dim",
            "learning_outcome_result_fact",
            "learning_outcome_rubric_criterion_dim",
            "learning_outcome_rubric_criterion_fact",
            "module_completion_requirement_dim",
            "module_completion_requirement_fact",
            "module_dim",
            "module_fact",
            "module_item_dim",
            "module_item_fact",
            "module_prerequisite_dim",
            "module_prerequisite_fact",
            "module_progression_completion_requirement_dim",
            "module_progression_completion_requirement_fact",
            "module_progression_dim",
            "module_progression_fact",
            "pseudonym_dim",
            "pseudonym_fact",
            "quiz_dim",
            "quiz_fact",
            "quiz_question_answer_dim",
            "quiz_question_answer_fact",
            "quiz_question_dim",
            "quiz_question_fact",
            "quiz_question_group_dim",
            "quiz_question_group_fact",
            "quiz_submission_dim",
            "quiz_submission_fact",
            "quiz_submission_historical_dim",
            "quiz_submission_historical_fact",
            "requests",
            "role_dim",
            "submission_comment_dim",
            "submission_comment_fact",
            "submission_dim",
            "submission_fact",
            "submission_file_fact",
            "user_dim",
            "wiki_dim",
            "wiki_fact",
            "wiki_page_dim",
            "wiki_page_fact"
        ]