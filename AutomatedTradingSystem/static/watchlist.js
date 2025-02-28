let portfolioData = [
    { code: 'AAPL', quantity: 50 },
    { code: 'GOOGL', quantity: 30 },
    { code: 'AMZN', quantity: 20 },
    { code: 'AAPL', quantity: 50 },
    { code: 'GOOGL', quantity: 30 },
    { code: 'AMZN', quantity: 20 },
    { code: 'AAPL', quantity: 50 },
    { code: 'GOOGL', quantity: 30 },
    { code: 'AMZN', quantity: 20 },
    { code: 'AAPL', quantity: 50 },
    { code: 'GOOGL', quantity: 30 },
    { code: 'AMZN', quantity: 20 },
    { code: 'AAPL', quantity: 50 },
    { code: 'GOOGL', quantity: 30 },
    { code: 'AMZN', quantity: 20 },
    { code: 'AAPL', quantity: 50 },
    { code: 'GOOGL', quantity: 30 },
    { code: 'AMZN', quantity: 20 },
    { code: 'AAPL', quantity: 50 },
    { code: 'GOOGL', quantity: 30 },
    { code: 'AMZN', quantity: 20 },
    { code: 'AAPL', quantity: 50 },
    { code: 'GOOGL', quantity: 30 },
    { code: 'AMZN', quantity: 20 }
];

document.addEventListener('DOMContentLoaded', function() {
    updatePortfolio();
});

function updatePortfolio() {
    const tableBody = document.getElementById('portfolio').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
    portfolioData.forEach(stock => {
        const newRow = tableBody.insertRow();
        newRow.innerHTML = `
            <td>${stock.code}</td>
            <td>${stock.quantity}</td>
            <td>0</td>
            <td>${stock.quantity}</td>
            <td>Enter Price</td>
            <td>Current Price</td>
            <td>Total Value</td>
            <td>Change%</td>
            <td>Proportion%</td>
            <td><button onclick="openSellDialog('${stock.code}', this)">Sell</button></td>
        `;
    });
}

// function sellStock(stockCode, buttonElement) {
//     const row = buttonElement.closest('tr');
//     let quantity = parseInt(row.cells[3].textContent);
//     if (quantity > 1) {
//         quantity -= 1; // Decrease stock quantity
//         row.cells[3].textContent = quantity;
//     } else {
//         row.parentNode.removeChild(row); // Remove the row if quantity goes to 0
//     }
// }
// Hàm xử lý sự kiện tìm kiếm mã cổ phiếu
function searchStock() {
  const input = document.getElementById('searchInput');
  const filter = input.value.toUpperCase();
  const table = document.getElementById('portfolio');
  const rows = table.getElementsByTagName('tr');

  // Lặp qua tất cả các hàng và ẩn hoặc hiển thị hàng tương ứng
  for (let i = 0; i < rows.length; i++) {
      const codeCell = rows[i].getElementsByTagName('td')[0];
      if (codeCell) {
          const codeText = codeCell.textContent || codeCell.innerText;
          if (codeText.toUpperCase().indexOf(filter) > -1) {
              rows[i].style.display = '';
          } else {
              rows[i].style.display = 'none';
          }
      }
  }
}

function openSellDialog(stockCode, buttonElement) {
  const row = buttonElement.closest('tr');
  const currentQuantity = parseInt(row.cells[3].textContent);
  const sellQuantity = prompt(`Nhập số lượng cổ phiếu muốn bán (tối đa ${currentQuantity}):`, currentQuantity);
  if (sellQuantity !== null) {
      const quantity = parseInt(sellQuantity);
      if (!isNaN(quantity) && quantity >= 1 && quantity <= currentQuantity) {
          const confirmSell = confirm(`Bạn có chắc chắn muốn bán ${quantity} cổ phiếu ${stockCode} không?`);
          if (confirmSell) {
              const newQuantity = currentQuantity - quantity;
              row.cells[3].textContent = newQuantity;
              if (newQuantity === 0) {
                  // Xoá dòng khi số lượng cổ phiếu giảm xuống 0
                  row.parentNode.removeChild(row);
              }
              // Ở đây bạn có thể thêm các xử lý khác như cập nhật dữ liệu bán cổ phiếu vào hệ thống của bạn
          }
      } else {
          alert('Số lượng không hợp lệ!');
      }
  }
}

function redirectToTransactionHistory() {
    // Chuyển hướng sang trang HTML mới
    window.location.href = "/lichsu";
}


