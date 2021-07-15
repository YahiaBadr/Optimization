import React, { useMemo } from "react";
import { useTable } from "react-table";
import styled from 'styled-components'

const Styles = styled.div`
  padding: 1rem;

  table {
    border-spacing: 0;
    border: 1px solid black;

    tr {
      :last-child {
        td {
          border-bottom: 0;
        }
      }
    }

    th,
    td {
      margin: 0;
      padding: 0.5rem;
      border-bottom: 1px solid black;
      border-right: 1px solid black;

      :last-child {
        border-right: 0;
      }
    }
  }
`

export default function ResultTable({ output }) {
	const data = useMemo(() => output.map(string => {
        let array = string.split(' ');
        return {
            req: array[0],
            branch: array[1],
            slot: array[2],
            counter: array[3],
        }
    }), [output]);
	const columns = useMemo(
		() => [
			{
				Header: "Request Id",
				accessor: "req"
			},
			{
				Header: "Branch No.",
				accessor: "branch"
			},
			{
				Header: "Slot No.",
				accessor: "slot"
			},
			{
				Header: "Counter No.",
				accessor: "counter"
			}
		],
		[]
	);

	const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
		useTable({ columns, data });

	return (
        <div
            style={{ display: "flex", justifyContent: "center", width: "fit-content", margin:"auto" }}
        >

        <Styles>
		<table {...getTableProps()} 
        >
			<thead>
				{headerGroups.map(headerGroup => (
					<tr {...headerGroup.getHeaderGroupProps()}>
						{headerGroup.headers.map(column => (
							<th
								{...column.getHeaderProps()}
							>
								{column.render("Header")}
							</th>
						))}
					</tr>
				))}
			</thead>
			<tbody {...getTableBodyProps()}>
				{rows.map(row => {
					prepareRow(row);
					return (
						<tr {...row.getRowProps()}>
							{row.cells.map(cell => {
								return (
									<td
										{...cell.getCellProps()}
									>
										{cell.render("Cell")}
									</td>
								);
							})}
						</tr>
					);
				})}
			</tbody>
		</table>
        </Styles>
        </div>

	);
}
