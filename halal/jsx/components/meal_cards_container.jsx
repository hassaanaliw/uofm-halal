/*
CourseTitle component for GradeGuide
 */

import React from 'react';
import PropTypes from 'prop-types';


class MealCardsContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {mealData: {}, isLoaded: false};
    }

    componentDidMount() {
    }


    componentDidUpdate() {
        if (isEmpty(this.props.mealData) && this.state.isLoaded === false) {
            console.log("Not gonna render");
            console.log(this.props.mealData);

            return;
        }

        if (this.state.isLoaded === false) {
            console.log("gonna render");
            this.setState({isLoaded: true});
        }

    }


    render() {
        if (isEmpty(this.props.mealData)) {
            // Whilst the API call hasn't been completed, keep displaying a loaded sign
            return ("Sorry! No Halal Meat Dishes being served on Campus This Day.");
        }


        var data = this.props.mealData;

        // Header Mapping. Use a unique color for all the dining halls to keep the
        // UX clean and easy
        var map = {
            "Bursley Dining Hall": "#673ab7",
            "South Quad Dining Hall": "#ff6a3b",
            "Mosher Jordan Dining Hall": "#009688",
            "East Quad Dining Hall": "#008eff",
            "Martha Cook Dining Hall": "#f93e7e",
            "Lawyers Club Dining Hall": "#322133",
            "North Quad Dining Hall": "#fdd835",
            "Twigs At Oxford": "#e91e63"
        }

        if (isEmpty(data)) {
            return ("Sorry! No Halal Meat Dishes being served on Campus This Day.");
        }

        return (

            // returns a selection menu for mobile
            <div className="row">
                {
                    data.map(function (item) {

                        var headerStyle = {'border-top': "8px solid " + map[item.dining_hall]};

                        return (
                            <div className="col-lg-4">
                                <div className="card">
                                    <div className="card-body meal-header"
                                         style={headerStyle}>
                                        <h5 className="card-title">{item.dish_name}</h5>
                                        <div className="card-subtitle">{item.dining_hall}</div>
                                    </div>

                                    <ul className="list-group list-group-flush">
                                        <li className="list-group-item"><strong>Station: </strong>{item.course_name}
                                        </li>
                                        <li className="list-group-item meal-name">
                                            <strong>Meal: </strong>{item.meal_name}</li>
                                        <li className="list-group-item"><strong>Allergens</strong></li>
                                    </ul>
                                    <div className="card-body">
                                        <div className="meal-hours">
                                            <div className="title">
                                                Hours
                                            </div>
                                            {item.hours.map(function (i) {
                                                return (<p><b>{i.name}</b>: {i.desc}</p>);
                                            })}

                                        </div>
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

MealCardsContainer.propTypes = {};

export default MealCardsContainer;


function isEmpty(obj) {
    for (var prop in obj) {
        if (obj.hasOwnProperty(prop))
            return false;
    }

    return true;
}