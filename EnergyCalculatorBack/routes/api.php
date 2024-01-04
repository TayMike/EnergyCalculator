<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\V1\UserController;
use App\Http\Controllers\Api\V1\StateController;
use App\Http\Controllers\Api\V1\CityController;
use App\Http\Controllers\Api\V1\FeeListController;

Route::prefix('v1')->group( function() {
    // Users
    Route::get('/users', [UserController::class, 'index']);
    Route::get('/users/{user}', [UserController::class, 'show']);
    Route::post('/users', [UserController::class, 'store']);

    // States
    Route::get('/states', [StateController::class, 'index']);
    // Route::get('/states/{state}', [StateController::class, 'show']);
    
    // Cities
    // Route::get('/cities', [CityController::class, 'index']);
    Route::get('/cities/{state}', [CityController::class, 'showFK']);
    // Route::get('/cities/{city}', [CityController::class, 'show']);
    
    // Fee_lists
    // Route::get('/fee_lists', [FeeListController::class, 'index']);
    Route::get('/fee_lists/{city}', [FeeListController::class, 'showFK']);
    // Route::get('/fee_lists/{feeList}', [FeeListController::class, 'show']);
});

// Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
//     return $request->user();
// });
