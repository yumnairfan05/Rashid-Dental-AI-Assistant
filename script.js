async function askQuestion() {

    const question = document.getElementById("question").value;

    if(question.trim() === ""){
        alert("Please enter a question.");
        return;
    }

    document.getElementById("answer").innerHTML = "Thinking...";

    try{

        const response = await fetch("http://127.0.0.1:8000/chat",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                question:question
            })

        });

        const data = await response.json();

        document.getElementById("answer").innerHTML = data.answer;

    }

    catch(error){

        document.getElementById("answer").innerHTML =
        "Unable to connect to backend.";

        console.log(error);

    }

}