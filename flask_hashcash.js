
function createCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function hash(puzzle,solution){
    return Sha1.hash(puzzle.concat(solution)); // btw this is in binary
}

function findHashcashSolution(params = {}){
    default_params = {puzzle:null, difficulty:5, solution:0, callback:null};
    for(k in default_params)
        if(params[k] == undefined)
            params[k] = default_params[k];
    var puzzle = params.puzzle,
        difficulty = params.difficulty,
        solution = params.solution,
        callback = params.callback;   
    
    // read current puzzle from cookies
    if(puzzle == null)
        puzzle = readCookie('hashcash_puzzle');
    if(puzzle == null)
        return;
    // if you have cached solution no need to continue seach
    if(hash(puzzle, readCookie('hashcash_solution')) == Array(difficulty+1).join("0"))
        return;

    // check solution from params
    var h = hash(puzzle,solution);
    // if the hash starts with *difficulty*(default = 1) of zeros - solution verified
    if(h.substring(0,difficulty) == Array(difficulty+1).join("0")){
        createCookie('hashcash_solution', solution); //store it as cookie
        if(callback)
            callback.call(solution);
    }else
        // continuing search
        setTimeout(function(){
            params.solution += 1 // try next number
            findHashcashSolution(params);
        }, 0);
}