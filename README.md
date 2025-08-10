# Streamlit AgGrid Data Table Demo

A demonstration of Streamlit application featuring interactive data tables with aggregations using `streamlit-aggrid` (which provides AG Grid functionality for Streamlit).

## Features

- Interactive data table with sorting, filtering, and selection
- Row and column aggregations (sum, average, count, etc.)
- Grouping and pivot functionality
- Export capabilities
- Custom cell renderers and editors
- Real-time data updates

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aggrid
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Project Structure

```
aggrid/
├── app.py                 # Main Streamlit application
├── data/
│   └── sample_data.py    # Sample data generation
├── components/
│   └── aggrid_table.py   # Reusable AG Grid components
├── requirements.txt      # Project dependencies
├── README.md            # This file
└── venv/               # Virtual environment
```

## Dependencies

- `streamlit`: Web app framework
- `streamlit-aggrid`: AG Grid integration for Streamlit
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `plotly`: Interactive visualizations (optional)

## Features Demonstrated

### Basic Table Features
- Column sorting and filtering
- Row selection (single/multiple)
- Cell editing
- Pagination

### Aggregation Features
- Column sum, average, min, max
- Row grouping with aggregations
- Pivot table functionality
- Custom aggregation functions

### Advanced Features
- Conditional formatting
- Custom cell renderers
- Export to CSV/Excel
- Real-time data updates
- Theme customization

## Example Data

The application uses sample sales data with the following columns:
- `Date`: Transaction date
- `Product`: Product name
- `Category`: Product category
- `Region`: Sales region
- `Sales Rep`: Salesperson name
- `Quantity`: Items sold
- `Unit Price`: Price per item
- `Total Amount`: Total transaction value
- `Profit Margin`: Profit percentage

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [streamlit-aggrid Documentation](https://github.com/PablocFonseca/streamlit-aggrid)
- [AG Grid Documentation](https://www.ag-grid.com/documentation/)
