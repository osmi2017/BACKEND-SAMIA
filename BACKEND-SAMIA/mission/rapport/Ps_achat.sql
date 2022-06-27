
CREATE   PROCEDURE Ps_validation_da

AS
BEGIN  
	BEGIN TRANSACTION
     

DECLARE 
	@NumDA varchar(50),
	@DateDA smalldatetime,
	@date_decision_dmg_dc date,
	@decision_dmg_dc   varchar(50),
	@nbrejour float,
	@numerojour int,
	@numerojourDateda int


DECLARE myCursor1 CURSOR LOCAL
FOR   
	    SELECT NumDA,DateDA ,date_decision_dmg_dc,decision_dmg_dc FROM vueValidationAchat   
		  
OPEN myCursor1


FETCH NEXT FROM myCursor1 INTO @NumDA,@DateDA,@date_decision_dmg_dc,@decision_dmg_dc

WHILE @@FETCH_STATUS = 0
	BEGIN

	    SET @numerojour =(select DATEPART(WEEKDAY, GETDATE()))

	    SET @numerojourDateda=(select DATEPART(WEEKDAY, @DateDA))

		IF (@numerojour<>1 AND @numerojourDateda<>5)
		BEGIN
		    SET @nbrejour=(select datediff(DAY, @DateDA,GETDATE()))

			IF @nbrejour>2
			   BEGIN
				   UPDATE  DemandeAchat SET  date_decision_dmg_dc=GETDATE() ,decision_dmg_dc='BON POUR ACCORD' , valider_dmg='VALIDE.AUTO',
				 obser_dmg_dc='VALIDATION AUTOMATIQUE DU SYSTEME'   where NumDA=@NumDA
	
			   END
			   
		END


	    FETCH NEXT FROM myCursor1 INTO @NumDA,@DateDA,@date_decision_dmg_dc,@decision_dmg_dc

 	END

CLOSE myCursor1
DEALLOCATE myCursor1

		  
IF @@ERROR <> 0
		BEGIN
			ROLLBACK TRANSACTION
		END
ELSE

		
		COMMIT TRANSACTION
	
		RETURN 
END

RETURN



