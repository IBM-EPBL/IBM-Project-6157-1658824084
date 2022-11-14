//////////////////////////////EXPENDITURE////////////////////////////////////////////
const balance = document.getElementById('balance')
const money_plus = document.getElementById('money-plus')
const money_minus = document.getElementById('money-minus')
const list = document.getElementById('list')
const form = document.getElementById('form')
const text = document.getElementById('text')
const amount = document.getElementById('amount')


const localStorageTransactions = JSON.parse(
    localStorage.getItem('transactions')
);

let transactions = localStorage.getItem('transactions') !== null ? localStorageTransactions : [];

// Add transaction
function addTransaction(e) {
    e.preventDefault();

    if(text.value.trim() === '' || amount.value.trim() === '') {
        alert('Please add a text and amount');
    }else {
        const transaction = {
            id: generateID(),
            text: text.value,
            amount: +amount.value
        };

        transactions.push(transaction);

        addTransactionDOM(transaction);

        updateValues()

        updateLocalStorage()

        text.value = ''
        amount.value = ''
    }
}

//generate random ID
function generateID() {
    return Math.floor(Math.random() * 100000000);
}

//Add transactions to DOM list
function addTransactionDOM(transaction) {
    //get sign
    const sign = transaction.amount < 0 ? '-' : '-';

    const item = document.createElement('li');

    // Add class based on value
    item.classList.add(transaction.amount < 0 ? 'minus' : 'minus');

    item.innerHTML = `
    
        ${transaction.text} <span>${sign}${Math.abs(transaction.amount)}</span>
        <button class="delete-btn" onclick="removeTransaction(${transaction.id})">x</button>
    `;

    list.appendChild(item);
    
}

//update the balance, income and expense
function updateValues() {
    const amounts = transactions.map(transaction => transaction.amount);

    const total = amounts.reduce((acc, item) => (item<0?acc += item:acc -= item), 0).toFixed(2);

    const income = 0;

    const expense = (
        amounts.filter(item => item < 0 || item>0).reduce((acc, item) => (acc += item), 0) * -1).toFixed(2);
    
    balance.innerText = `$${total}`;
    money_plus.innerText = `$${income}`;
    money_minus.innerText = `$${expense}`;

}

//Remove transaction by ID
function removeTransaction(id) {
    transactions = transactions.filter(transaction => transaction.id !== id);

    updateLocalStorage();

    init();
}

//update local storage transactions
function updateLocalStorage() {
    localStorage.setItem('transactions', JSON.stringify(transactions));
}

//Init app
function init() {
    list.innerHTML = '';

    transactions.forEach(addTransactionDOM);
    updateValues()
}

init();
form.addEventListener('submit', addTransaction);

/////////////////////////////////WALLET PAGE//////////////////////////////////////////////////////////

   
    
   function bal() {
    var x = document.getElementById("balance").value;
    
    y=parseFloat(x);
    if(isNaN(y))
    {
        y=0;
    }
    var bal=parseInt(document.getElementById("bal").innerHTML)+y;
    
    document.getElementById("bal").innerHTML=bal;
    
   // document.getElementById("bal").innerHTML=parseInt(document.getElementById("bal").innerHTML)+y;
    }

function fun() {
  
var x = document.getElementById("limit").value;
document.getElementById("lim").innerHTML=x;
alert ("LIMIT "+x+" SUCESSFULLY ADDED!");
}