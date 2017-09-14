function setHandlers(){
	$('#id_PresetExecution').on("change", function(){
		var opcao = $('#id_PresetExecution').val();
		console.log(opcao);
		var algSelect = $('#id_PresetExecution option:selected').text();
		if(opcao){
			$("#id_Algorithm option").filter(function() {
		   		return $(this).text() == algSelect; 
			}).prop('selected', true);
			$("#id_opt").val('');
			$("#id_Algorithm").prop('disabled', true);	
			$("#id_opt").prop('disabled', true);
			$("#id_fileIn").prop('disabled', true);

		}else{
			$('select#id_Algorithm').prop('selectedIndex', 0);
			$("#id_opt").val('');	
			$("#id_Algorithm").prop('disabled', false);	
			$("#id_opt").prop('disabled', false);
			$("#id_fileIn").prop('disabled', false	);
		}
	});
};

hlpButtom = document.getElementById('showDesc')
div = document.getElementById('hlpAlg');

hlpButtom.addEventListener("click", function(){
	div.style.display = (div.style.display === 'block') ? 'none':'block';
})

setHandlers();


// setTriggers();
