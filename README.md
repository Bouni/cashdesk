# Reaktor23 cashdesk

*cashdesk* is a web application that allows us to manage the payment of drinks (and potentially other things in the future) on a trust base.

It runs as a docker container on our actse server and can be used on mobile devices as well as laptops and computers.

![Main screen](cashdesk1.png?raw=true "The main screen")

Because it is operated on a trust base, we have no login or other authetication process.
A user simply selects his account.

![Account screen](cashdesk2.png?raw=true "The account screen")

Once an account is selected the user sees his funds, a log of the recent transactions and two buttons.
One button for vending a drink one for toping up the funds.

![Vend screen](/cashdesk3.png?raw=true "The vend screen")

On the vend screen the user selects the drink of choice, that subtracts the price of the drink from his funds

![Funds screen](/cashdesk4.png?raw=true "The funds screen")

The funds screen works in the same way, a user clicks the amount that should get added to the account.
