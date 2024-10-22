-- This script creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE avg_weighted_score FLOAT;

    DECLARE done INT DEFAULT FALSE;
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN user_cursor;

    user_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;

        SELECT SUM(score * weight) / SUM(weight)
        INTO avg_weighted_score
        FROM corrections
        LEFT JOIN projects
        ON projects.id = corrections.project_id
        WHERE corrections.user_id = user_id;

        UPDATE users SET average_score = IFNULL(avg_weighted_score, 0)
        WHERE id = user_id;
    END LOOP;

    CLOSE user_cursor;
END $$

DELIMITER ;
