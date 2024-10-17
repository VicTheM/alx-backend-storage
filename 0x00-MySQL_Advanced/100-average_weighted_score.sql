-- This script creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_weighted_score FLOAT;

    SELECT SUM(score * weight) / SUM(weight)
    INTO avg_weighted_score
    FROM corrections
    LEFT JOIN projects
    ON projects.id = corrections.project_id
    WHERE corrections.user_id = user_id;

    UPDATE users SET average_score = avg_weighted_score
    WHERE id = user_id;

END $$

DELIMITER ;
