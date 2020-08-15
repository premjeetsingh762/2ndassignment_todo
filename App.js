import React from 'react';


class Todos extends React.Component {
    constructor(props) {
        super(props);
        this.state = { todos: [], text: '' };
        this.removeTodo = this.removeTodo.bind(this);
    }

    additionTodo(e) {
        e.preventDefault();
        this.setState({ 
        	todos: [ this.state.text, ...this.state.todos ],
        	text: ''
        });
    }

    deleteTodo(name, i){
        let todos = this.state.todos.slice();
        todos.splice(i, 1);
        this.setState({
            todos
        });
    }

    todoUpdate(e) {
        this.setState({ text: e.target.value})
    }

    render() {
        return(
            <div className="card d-flex main-header">
            <div className="card-body">
                <form className="form-group"onSubmit = {(e) => this.addTodo(e)}>
                    <input className="form-control"
                        placeholder="Add Todo"
                        value={this.state.text}
                        onChange={(e) => {this.updateValue(e)}}
                    />
                    <button className="btn btn-primary" type="submit">Add Todo</button>
                </form>
                <TodoList todos={this.state.todos} removeTodo={this.removeTodo}/>
            </div>
            </div>
        );
    }
}

class TodoList extends React.Component {

    deleteItem(item, i) {
        this.props.removeTodo(item, i);
    }

    render() {
        return(
            <ul>
                { this.props.todos.map((todo,i) => {
                    return <li onClick={() => { this.deleteItem(todo, i)}} key={i}>{ todo }</li>
                })}
            </ul>
        );
    }
}

export default Todos;
