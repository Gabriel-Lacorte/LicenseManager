function login(username, password) {
    return $.ajax({
        url: '/api/auth/login',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            username: username,
            password: password
        }),
        dataType: 'json',
        success: function(response) {
            return response;
        }
    });
}

function logout() {
    return $.ajax({
        url: '/api/auth/logout',
        type: 'POST',
        dataType: 'json',
        success: function(response) {
            return response;
        }
    });
}

function listProducts() {
    return $.ajax({
        url: '/api/products',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            return response;
        }
    });
}

function createProduct(name, description) {
    return $.ajax({
        url: '/api/products',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            name: name,
            description: description
        }),
        dataType: 'json',
        success: function(response) {
            return response;
        }
    });
}

function getProductById(id) {
    return $.ajax({
        url: '/api/products/' + id,
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            return response;
        }
    });
}

function deleteProductById(id) {
    return $.ajax({
        url: '/api/products/' + id,
        type: 'DELETE',
        dataType: 'json',
        success: function(response) {
            return response;
        }
    });
}

// TODO
function getKey(key) {
    return $.ajax({
        url: '/api/keys/' + key,
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            return response;
        }
    });
}

// TODO
function deleteKey(key) {
    return $.ajax({
        url: '/api/keys/' + key,
        type: 'DELETE',
        dataType: 'json',
        success: function(response) {
            return response;
        }
    });
}

// TODO
function increaseKeyPeriod(key, period) {
    return $.ajax({
        url: '/api/keys/' + key,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify({
            period: period
        }),
        dataType: 'json',
        success: function(response) {
            return response;
        }
    });
}

function createKey(product_id, period) {
    return $.ajax({
        url: '/api/keys',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            product_id: product_id,
            period: period
        }),
        dataType: 'json',
        success: function(response) {
            return response;
        }
    });
}