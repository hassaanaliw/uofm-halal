import 'babel-polyfill'
import React from 'react';
import ReactDOM from 'react-dom';
import MealCardsContainer from './components/meal_cards_container';


class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            halalData: {},
            currentData: {},
            isLoaded: false,
            url: "/halal/2018/04/12" // Hardcoded for now since we have no current menus
        };
        this.renderChildren = this.renderChildren.bind(this);
        this.updateDate = this.updateDate.bind(this);

    }

    fetchData() {
        fetch(this.state.url)
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                // setState calls the render function again
                this.setState({
                    halalData: data,
                    currentData: data.data[0],
                    currentDate: data.data[0]["date"],
                    currentIndex: 0,
                    isLoaded: true
                });

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


    updateDate(action) {
        if (action === "previous") {
            if (this.state.currentIndex === 0) {
                // Cant move further back
                return
            } else {
                this.setState({
                    currentData: this.state.halalData.data[this.state.currentIndex - 1],
                    currentIndex: this.state.currentIndex - 1
                })
            }
        } else {
            if (this.state.currentIndex === 5) {
                // Cant move further forward
                return
            } else {
                this.setState({
                    currentData: this.state.halalData.data[this.state.currentIndex + 1],
                    currentIndex: this.state.currentIndex + 1
                })
            }
        }
    }


    render() {
        if (!this.state.isLoaded) {
            // Whilst the API call hasn't been completed, keep displaying a loaded sign
            return (
                'Loading...'
            );
        }

        var data = this.state.currentData;

        //  settings to formate the date strings included in the JSON
        var options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };


        var date = new Date(data.date);
        var _this = this;

        return (

            // returns a selection menu for mobile
            <div onKeyDown={(event) => {
                if (event.keyCode === "37") {
                    _this.updateDate("previous")
                } else if (event.keyCode === "39") {
                    _this.updateDate("next")
                }
            }}>


                <div id="meal-holder-primary">
                    <div className="meals-holder">

                        <div className="meal-date">
                            <h2>{date.toLocaleDateString("en-US", options)}</h2>

                        </div>

                        <div className="date-buttons">
                            <div onClick={() => _this.updateDate("previous")}
                                 className="button-date button-date-prev">
                                Previous
                            </div>
                            <div onClick={() => _this.updateDate("next")}
                                 className="button-date button-date-next">Next
                            </div>

                        </div>

                        <div className="meal-cards-holder">
                            <MealCardsContainer
                                mealData={data.halal_dishes}/>
                        </div>

                    </div>
                </div>

                );


            </div>


        );

    }

}

ReactDOM.render(<Home/>, document.getElementById('main-container'));