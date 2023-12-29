<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use App\Models\City;

class CityController extends Controller
{
    /**
     * Display the specified resource.
     */
    public function index()
    {
        $states = City::all();
        // $states = DB::select('select * from states');
 
        return view('simulador', ['states' => $states]);
    }
}
