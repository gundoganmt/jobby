var form = document.getElementById('post_task');
form.addEventListener('submit', validate);

function validate(e){

  var project_name = form.project_name.value;
  var category = form.category.value;
  var budget_min = parseInt(form.budget_min.value);
  var budget_max = parseInt(form.budget_max.value);
	var description = form.description.value;
  var skills = form.skillsHidden;
  skillsText = document.getElementsByClassName('keyword-text');

  var errProjectName = document.getElementById('errorProjectName');
  var errCategory = document.getElementById('errorCategory');
  var errorBudget_min = document.getElementById('errorBudget_min');
  var errorBudget_max = document.getElementById('errorBudget_max');
  var errSkills = document.getElementById('errorSkills');
  var errorDescription = document.getElementById('errorDescription');

  if (project_name.length < 3){
    errProjectName.innerText = "* Proje ismi çok kısa";
    e.preventDefault();
  }

  else{
    errProjectName.innerText = "";
  }
  //
  if (!category){
    errCategory.innerText = "* Bir kategori seçin";
    e.preventDefault();
  }

  else{
    errCategory.innerText = "";
  }
  //
	if (budget_min != "" && budget_max != ""){

		if(budget_min < 10){
			errorBudget_min.innerText = "* En dusuk proje butçesi 10 TL olmalı";
	    e.preventDefault();
		}
		else{
	    errorBudget_min.innerText = "";
	  }
		if (budget_max > 100000){
	    errorBudget_max.innerText = "* En buyuk proje butçesini 100 bin TL olmalı";
	    e.preventDefault();
	  }

	  else{
	    errorBudget_max.innerText = "";
	  }
		if (budget_min >= budget_max){
	    errorBudget_max.innerText = "* Minimum değer maximumdan buyuk olamaz";
	    e.preventDefault();
	  }

	  else{
	    errorBudget_max.innerText = "";
	  }
	}

	if (description.length < 30){
		errorDescription.innerText = "* Açıklama en az 30 karakter içermeli";
		e.preventDefault()
	}
	else{
		errorDescription.innerText = "";
	}

  skills.value = "";

  if(skillsText.length > 5){
    errSkills.innerText = "* En fazla 5 yetenek yazmalısın"
    e.preventDefault();
  }

  if(skillsText.length == 0){
    errSkills.innerText = "* En az bir yetenek yazmalısın";
    e.preventDefault();
  }

  if(skillsText.length > 0 && skillsText.length < 6){
    errSkills.innerText = "";
  }


  for (item of skillsText){
    skills.value += item.innerText + "*";
  }

  return true;
}
