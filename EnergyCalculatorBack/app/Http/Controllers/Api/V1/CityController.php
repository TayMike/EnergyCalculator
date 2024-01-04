<?php

namespace App\Http\Controllers\API\V1;

use App\Http\Controllers\Controller;
use App\Http\Resources\V1\CityResource;
use App\Models\City;
use Illuminate\Http\Request;

class CityController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return CityResource::collection(City::with('state')->get());
    }

    /**
     * Display the specified resource with a foreign key.
     */
    public function showFK(string $id)
    {
        return CityResource::collection(City::where('state_id', $id)->with('state')->get());
    }

    /**
     * Display the specified resource.
     */
    public function show(City $city)
    {
        return new CityResource($city);
    }
}
