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

function setAlgorithmDescription(){
	hlpButtom = document.getElementById('showDesc')
	div = document.getElementById('hlpAlg');

	hlpButtom.addEventListener("click", function(){
	div.style.display = (div.style.display === 'block') ? 'none':'block';
	})
}

function randomColor(type){
	//pick a "red" from 0 - 255
	var r = Math.floor(Math.random() * 256);
	//pick a "red" from 0 - 255
	var g = Math.floor(Math.random() * 256);
	//pick a "red" from 0 - 255
	var b = Math.floor(Math.random() * 256);
	
	return ["rgba(" + r + ", " + g + ", " + b + ", 1)","rgba(" + r + ", " + g + ", " + b + ", 0.1)"];
	
}


function drawStatisticsChart(){
	
	var chartCanvas= document.getElementById("appChart").getContext('2d');
	var chartLabel = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'];
	var chartDataset = [];

	for(var key in dt){
		var algDataset = {}
		if (dt.hasOwnProperty(key)){
        	var value=dt[key];
        	
        	algDataset['label'] = key;
        	algDataset['data'] = value;

        	var dataColor = randomColor();

        	algDataset['borderColor'] = dataColor[0];
        	// algDataset['backgroundColor'] = dataColor[1];

    	}
    	chartDataset.push(algDataset);
	}
 
 	// draw the chart
	var productsChart = new Chart(chartCanvas,{
    	type: 'line',
    	data: {
        	labels: chartLabel,
        	datasets: chartDataset
    	},
    	options: {
  			title: {
    			display: true,
    			text: 'Número de execuções dos algoritmos - 2017'
  			},
  			scales:{
  				xAxes: [{
                	gridLines: {
                    	display:false
                	}
            	}],
    			yAxes: [{
                	gridLines: {
                    	display:false
                	}   
            	}]
  			}
		}
	});
}


// Call Functions
// setHandlers();

if(document.getElementById('showDesc')){
	setAlgorithmDescription();	
}

else if(document.getElementById("appChart")){
	 drawStatisticsChart();
}

// setTriggers();
