<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\StateController;
use App\Http\Controllers\CityController;
use App\Http\Controllers\FeeListController;

Route::get('/', function(){
    return view('home');
});

Route::get('/simulador', [FeeListController::class, 'index']);

// Route::get('/simulador', function(){
//     return view('simulador');
// });