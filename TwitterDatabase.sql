/* Design and build a database to store key information about your tweets, 
including the ID, the text of the tweet, 
the user who sent the tweet, 
when it was sent, and the location that was tracked (if any).  
Store other elements of the tweet as you feel appropriate. 
The database also needs to store the sentiment score and key phrases 
that are returned from the Microsoft API’s.
*/

CREATE TABLE Tweets (
    tweetID int identity(1,1),
    tweetText varchar(MAX),
    userName varchar(MAX),
    tweetDate date,
    tweetLocation varchar(MAX),
    sentimentScore varchar(MAX),
    keyPhrases varchar(MAX)
)

--Store data 
GO
CREATE OR ALTER PROCEDURE addTweets
		@tweetText VARCHAR(MAX),
		@userName VARCHAR(25),
		@tweetDate Date,
		@tweetLocation VARCHAR(MAX),
		@sentimentScore VARCHAR(MAX),
		@keyPhrases VARCHAR(MAX)
	AS
	BEGIN
		SELECT
		*
		FROM
			Tweets
		WHERE
			tweetText = @tweetText
			AND
			userName = @userName
			AND
			tweetDate = @tweetDate
			AND 
			tweetLocation = @tweetLocation
			AND
			sentimentScore = @sentimentScore
			AND
			keyPhrases = @keyPhrases
END

-- Retrieve Data
GO
CREATE PROCEDURE GetTweets
AS
BEGIN
	SELECT *
	FROM Tweets
END
GO

-- Get data using Stored procedure
EXEC GetTweets


--SELECT * FROM Tweets
--DROP TABLE Tweets

