import 'babel-polyfill'
import React from 'react';
import ReactDOM from 'react-dom';
import MealCardsContainer from './components/meal_cards_container';


class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            halalData: {},
            isLoaded: false,
            url: "/halal/2018/04/12" // Hardcoded for now since we have no current menus
        };
        this.renderChildren = this.renderChildren.bind(this);

    }

    fetchData() {
        fetch(this.state.url)
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                // setState calls the render function again
                this.setState({halalData: data, isLoaded: true});

            })
            .catch(error => console.log(error));
    }

    renderChildren() {

    }

    componentDidMount() {
        this.fetchData();
        this.renderChildren();

    }


    componentDidUpdate() {
        this.renderChildren();
    }


    render() {
        if (!this.state.isLoaded) {
            // Whilst the API call hasn't been completed, keep displaying a loaded sign
            return (
                'Loading...'
            );
        }

        var data = this.state.halalData.data;

        //  settings to formate the date strings included in the JSON
        var options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};


        return (

            // returns a selection menu for mobile
            <div>
                {
                    data.map(function (item) {
                        var date = new Date(item.date);
                        return (
                            <div id="meal-holder-primary">
                                <div className="meals-holder">

                                    <div className="meal-date">
                                        <h2>{date.toLocaleDateString("en-US", options)}</h2>
                                    </div>

                                    <div className="meal-cards-holder">
                                        <MealCardsContainer mealData={item.halal_dishes}/>
                                    </div>

                                </div>
                            </div>

                        );
                    })
                }
            </div>


        );

    }

}

ReactDOM.render(<Home/>, document.getElementById('main-container'));